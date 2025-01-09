import typing

import numpy as np

_maybe_np_T = typing.Union[np.ndarray, int]


class hybrid_algo:

    _algos: typing.List[typing.Any]
    _fenceposts: typing.List[int]
    _chunk_algo_indices: typing.List[int]

    def __init__(
        self: "hybrid_algo",
        *layout: list,
    ) -> None:
        self._algos = list(layout[1::2])
        self._fenceposts = list(layout[::2])
        self._chunk_algo_indices = [
            index
            for index, __ in enumerate(self._algos)
            for __ in range(*self._fenceposts[index : index + 2])
        ]

        if not self._algos:
            raise ValueError
        if not len(self._fenceposts) >= 2:
            raise ValueError
        if not all(val >= i for i, val in enumerate(self._fenceposts)):
            raise ValueError

    def _get_num_chunks(self: "hybrid_algo") -> int:
        return self._fenceposts[-1]

    def _get_algo_index(self: "hybrid_algo", T: _maybe_np_T) -> _maybe_np_T:
        leftover = T % self._get_num_chunks()
        return self._chunk_algo_indices[leftover]

    def _get_adj_T(
        self: "hybrid_algo", T: _maybe_np_T, index: _maybe_np_T
    ) -> _maybe_np_T:
        begin_chunk = self._fenceposts[index]
        end_chunk = self._fenceposts[index + 1]
        span_chunk_length = end_chunk - begin_chunk
        num_chunks = self._get_num_chunks()

        T_ref = T + num_chunks - end_chunk
        assert T_ref >= 0
        num_whole_rounds = T // num_chunks
        partial_chunks = sorted(
            (0, T % num_chunks - begin_chunk, span_chunk_length),
        )[1]

        return num_whole_rounds * span_chunk_length + partial_chunks

    def _get_span_scale(self: "hybrid_algo", S: int) -> _maybe_np_T:
        num_chunks = self._get_num_chunks()
        if not S % num_chunks == 0:
            raise ValueError
        return S // num_chunks

    def _get_span_length(
        self: "hybrid_algo", S: int, index: _maybe_np_T
    ) -> _maybe_np_T:
        span_scale = self._get_span_scale(S)
        begin_chunk = self._fenceposts[index]
        end_chunk = self._fenceposts[index + 1]
        return span_scale * (end_chunk - begin_chunk)

    def _get_span_offset(
        self: "hybrid_algo", S: int, index: _maybe_np_T
    ) -> _maybe_np_T:
        span_scale = self._get_span_scale(S)
        begin_chunk = self._fenceposts[index]
        return span_scale * begin_chunk

    def assign_storage_site(
        self: "hybrid_algo", S: int, T: int
    ) -> typing.Optional[int]:
        index = self._get_algo_index(T)
        algo = self._algos[index]

        span_length = self._get_span_length(S, index)
        T_adj = self._get_adj_T(T, index)
        span_site = algo.assign_storage_site(span_length, T_adj)

        span_offset = self._get_span_offset(S, index)
        return span_offset + span_site if span_site is not None else None

    def assign_storage_site_batched(
        self: "hybrid_algo", S: int, T: _maybe_np_T
    ) -> np.ndarray:
        raise NotImplementedError

    def get_ingest_capacity(
        self: "hybrid_algo", S: int
    ) -> typing.Optional[int]:
        span_lengths = (
            self._get_span_length(S, i) for i, __ in enumerate(self._algos)
        )
        ingest_capacities = (
            algo.get_ingest_capacity(span_length)
            for span_length, algo in zip(span_lengths, self._algos)
        )
        num_chunks = self._get_num_chunks()
        return min(
            (
                capacity * num_chunks + self._fenceposts[i]
                for i, capacity in enumerate(ingest_capacities)
                if capacity is not None
            ),
            default=None,
        )

    def has_ingest_capacity(self: "hybrid_algo", S: int, T: int) -> bool:
        num_chunks = self._get_num_chunks()
        for T_ in range(max(0, T - num_chunks + 1), T + 1):
            index = self._get_algo_index(T_)
            if not self._algos[index].has_ingest_capacity(
                self._get_span_length(S, index),
                self._get_adj_T(T_, index),
            ):
                return False
        return True

    def lookup_ingest_times(
        self: "hybrid_algo", S: int, T: int
    ) -> typing.Iterable[typing.Optional[int]]:
        for index, algo in enumerate(self._algos):
            adj_T = self._get_adj_T(T, index)
            span_length = self._get_span_length(S, index)
            for Tbar in algo.lookup_ingest_times(span_length, adj_T):
                num_chunks = self._get_num_chunks()
                begin_chunk = self._fenceposts[index]
                end_chunk = self._fenceposts[index + 1]
                span_chunk_length = end_chunk - begin_chunk
                if Tbar is not None:
                    yield begin_chunk + (
                        (Tbar // span_chunk_length) * num_chunks
                        + Tbar % span_chunk_length
                    )
                else:
                    yield None

    def lookup_ingest_times_eager(
        self: "hybrid_algo", S: int, T: int
    ) -> typing.List[int]:
        if T < S:
            raise ValueError("T < S not supported for eager lookup")
        return list(self.lookup_ingest_times(S, T))

    def lookup_ingest_times_batched(
        self: "hybrid_algo",
        S: int,
        T: np.ndarray,
        parallel: bool = True,
    ) -> np.ndarray:
        res = np.empty((T.size, S), dtype=np.uint64)
        for index, algo in enumerate(self._algos):
            adj_T = self._get_adj_T(T, index)
            span_length = self._get_span_length(S, index)
            for Tbar in algo.lookup_ingest_times_batched(
                span_length,
                adj_T,
                parallel=parallel,
            ):
                num_chunks = self._get_num_chunks()
                begin_chunk = self._fenceposts[index]
                end_chunk = self._fenceposts[index + 1]
                span_chunk_length = end_chunk - begin_chunk

                subres = (
                    begin_chunk
                    + (Tbar // span_chunk_length) * num_chunks
                    + Tbar % span_chunk_length
                )

                span_offset = self._get_span_offset(S, index)
                span_length = self._get_span_length(S, index)
                res[span_offset : span_offset + span_length] = subres

        return res
