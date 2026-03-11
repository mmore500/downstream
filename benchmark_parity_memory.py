"""Benchmark memory usage of parity checking: before vs after fix.

Compares the old approach (polars ops in worker threads, all submitted
eagerly via pool.map) against the new approach (polars collection in
main thread, bounded submission of numpy-only work to thread pool).

Uses subprocess isolation so each approach starts from a clean memory
state and RSS/VmPeak measurements are accurate.

Usage:
    python benchmark_parity_memory.py
"""

import json
import subprocess
import sys

_WORKER_SCRIPT = r'''
import gc
import json
import os
import resource
import sys
import threading
import time
from concurrent import futures
from unittest import mock

import numpy as np
import polars as pl

import downstream
from downstream._auxlib._iter_slices import iter_slices
from downstream.dataframe._unpack_data_packed import (
    _collect_chunk,
    _compute_parity_chunk,
    _compute_parity_numpy_only,
    _deserialize_h_matrix,
)


def _get_vm_peak_kb():
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmPeak:"):
                    return int(line.split()[1])
    except Exception:
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def _get_vm_rss_kb():
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
    except Exception:
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def _sample_rss_loop(results, stop_event, interval=0.02):
    peak = 0
    while not stop_event.is_set():
        rss = _get_vm_rss_kb()
        if rss > peak:
            peak = rss
        time.sleep(interval)
    results["sampled_peak_rss_kb"] = peak


def _make_large_df(n_rows, hex_width):
    rng = np.random.default_rng(42)
    hex_vals = [rng.bytes(hex_width // 2).hex() for _ in range(n_rows)]
    bits = hex_width * 4
    n_rules = 4
    h_rows = []
    for i in range(n_rules):
        row = [0] * bits
        for j in range(i, bits, n_rules):
            row[j] = 1
        h_rows.append(" ".join(str(x) for x in row))
    h_matrix_str = "\n".join(h_rows)
    storage_bits = 128
    t_bits = 16
    return pl.DataFrame({
        "dstream_algo": ["dstream.steady_algo"] * n_rows,
        "downstream_version": [downstream.__version__] * n_rows,
        "data_hex": hex_vals,
        "dstream_storage_bitoffset": [0] * n_rows,
        "dstream_storage_bitwidth": [storage_bits] * n_rows,
        "dstream_T_bitoffset": [storage_bits] * n_rows,
        "dstream_T_bitwidth": [t_bits] * n_rows,
        "dstream_S": [storage_bits // 8] * n_rows,
        "downstream_data_parity0_rule": [h_matrix_str] * n_rows,
    })


def _old_worker(args):
    """OLD approach: polars collect + str.join in worker thread."""
    group_slice, h_matrix, bits_per_row = args
    chunk = group_slice.select(
        "data_hex", "_downstream_parity_idx",
    ).collect()
    concat_hex = chunk.select(pl.col("data_hex").str.join("")).item()
    chunk_indices = chunk["_downstream_parity_idx"].to_numpy()
    row_violations = _compute_parity_chunk(
        concat_hex, h_matrix, bits_per_row,
    )
    return chunk_indices, row_violations


def run(n_rows, hex_width, mp_pool_size, max_concat_bytes, use_old):
    df = _make_large_df(n_rows, hex_width)
    gc.collect()

    with mock.patch.dict(
        os.environ,
        {"OPENBLAS_NUM_THREADS": "1"} if mp_pool_size > 1 else {},
    ):
        df_len = len(df)
        parity_result = np.zeros(df_len, dtype=int)

        indexed = (
            df.lazy()
            .with_row_index("_downstream_parity_idx")
            .filter(
                pl.col("downstream_data_parity0_rule").is_not_null()
                & (
                    pl.col("downstream_data_parity0_rule")
                    .cast(pl.String)
                    .str.len_bytes()
                    > 0
                ),
            )
        )

        unique_rules = (
            indexed.select("downstream_data_parity0_rule")
            .unique().collect().to_series().to_list()
        )

        sample_results = {}
        stop_event = threading.Event()
        sampler = threading.Thread(
            target=_sample_rss_loop,
            args=(sample_results, stop_event),
        )
        sampler.start()

        for h_matrix_str in unique_rules:
            group = indexed.filter(
                pl.col("downstream_data_parity0_rule") == h_matrix_str,
            )
            nrow_group = group.select(pl.len()).collect().item()
            h_matrix = _deserialize_h_matrix(str(h_matrix_str))

            hex_len = (
                group.select(pl.col("data_hex").str.len_bytes().first())
                .collect().item()
            )
            bits_per_row = hex_len * 4

            nrow_chunk = max(1, max_concat_bytes // hex_len)
            nrow_chunk = min(
                nrow_chunk, max(1, nrow_group // mp_pool_size),
            )

            if use_old:
                # OLD: eager pool.map, polars in worker threads
                work_items = (
                    (group[s], h_matrix, bits_per_row)
                    for s in iter_slices(nrow_group, nrow_chunk)
                )
                with futures.ThreadPoolExecutor(
                    max_workers=mp_pool_size,
                ) as pool:
                    for ci, rv in pool.map(_old_worker, work_items):
                        parity_result[ci] = rv
            else:
                # NEW: bounded submission, polars in main thread
                chunk_iter = iter(iter_slices(nrow_group, nrow_chunk))
                with futures.ThreadPoolExecutor(
                    max_workers=mp_pool_size,
                ) as pool:
                    pending = set()
                    for chunk_slice in chunk_iter:
                        ci, ch = _collect_chunk(group, chunk_slice)
                        fut = pool.submit(
                            _compute_parity_numpy_only,
                            ci, ch, h_matrix, bits_per_row,
                        )
                        pending.add(fut)
                        if len(pending) >= mp_pool_size:
                            break

                    while pending:
                        done, pending = futures.wait(
                            pending,
                            return_when=futures.FIRST_COMPLETED,
                        )
                        for fut in done:
                            ci, rv = fut.result()
                            parity_result[ci] = rv
                        for chunk_slice in chunk_iter:
                            ci, ch = _collect_chunk(
                                group, chunk_slice,
                            )
                            fut = pool.submit(
                                _compute_parity_numpy_only,
                                ci, ch, h_matrix, bits_per_row,
                            )
                            pending.add(fut)
                            if len(pending) >= mp_pool_size:
                                break

        stop_event.set()
        sampler.join()

    vm_peak = _get_vm_peak_kb()
    sampled_peak = sample_results.get("sampled_peak_rss_kb", 0)

    result = {
        "vm_peak_kb": vm_peak,
        "sampled_peak_rss_kb": sampled_peak,
        "parity_sum": int(parity_result.sum()),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    n_rows = int(sys.argv[1])
    hex_width = int(sys.argv[2])
    mp_pool_size = int(sys.argv[3])
    max_concat = int(sys.argv[4])
    use_old = sys.argv[5] == "old"
    run(n_rows, hex_width, mp_pool_size, max_concat, use_old)
'''


def run_in_subprocess(n_rows, hex_width, pool_size, max_concat, mode):
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            _WORKER_SCRIPT,
            str(n_rows),
            str(hex_width),
            str(pool_size),
            str(max_concat),
            mode,
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        print(f"STDERR: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Subprocess failed: {result.stderr}")
    return json.loads(result.stdout.strip())


def main():
    configs = [
        (200_000, 64, 8, 128 * 1024 * 1024),
        (200_000, 256, 8, 128 * 1024 * 1024),
        (500_000, 256, 8, 128 * 1024 * 1024),
    ]

    for n_rows, hex_width, pool_size, max_concat in configs:
        data_mb = n_rows * hex_width / (1024 * 1024)
        print(f"\n{'='*65}")
        print(
            f"Config: {n_rows:,} rows x {hex_width} hex chars, "
            f"{pool_size} threads, "
            f"{max_concat // (1024*1024)} MB max concat",
        )
        print(f"Total data_hex: {data_mb:.1f} MB")
        print(f"{'='*65}")

        old = run_in_subprocess(
            n_rows,
            hex_width,
            pool_size,
            max_concat,
            "old",
        )
        new = run_in_subprocess(
            n_rows,
            hex_width,
            pool_size,
            max_concat,
            "new",
        )

        print(
            f"  OLD: VmPeak={old['vm_peak_kb']//1024} MB, "
            f"sampled peak RSS={old['sampled_peak_rss_kb']//1024} MB",
        )
        print(
            f"  NEW: VmPeak={new['vm_peak_kb']//1024} MB, "
            f"sampled peak RSS={new['sampled_peak_rss_kb']//1024} MB",
        )

        if new["vm_peak_kb"] > 0:
            ratio = old["vm_peak_kb"] / new["vm_peak_kb"]
            print(f"  VmPeak reduction: {ratio:.2f}x")
        if new["sampled_peak_rss_kb"] > 0:
            ratio = old["sampled_peak_rss_kb"] / new["sampled_peak_rss_kb"]
            print(f"  Sampled RSS reduction: {ratio:.2f}x")
        print(
            f"  Results match: " f"{old['parity_sum'] == new['parity_sum']}",
        )


if __name__ == "__main__":
    main()
