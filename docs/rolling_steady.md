# Rolling + delayed steady, without metadata or relocation

This construction has a closed-form, loop-free selector. It uses exactly
`S` payload slots, one payload write per selected arrival, and no payload
reads, relocation, stored timestamps, slot maps, or lookup tables. Its only
inputs are the ordinary stream-depth counter `T` and fixed buffer size `S`.

The implementation is exposed as the module
`downstream.dstream.rolling_steady_algo`, following the same interface as
`steady_algo`:

```python
from downstream.dstream import rolling_steady_algo
from downstream.dsurf import Surface

surface = Surface(rolling_steady_algo, 16)
for t in range(64):
    surface.ingest_one(t)
assert list(surface) == list(surface.lookup())
```

## Retention contract

Let `S = 2m`, where `m = 2**s >= 2`. After `T` arrivals, define
`b = max(0, T-m)`, the length of the prefix outside the rolling window.
The retained arrival-index set is exactly

```
{b, ..., T-1}  union  steady_algo.lookup_ingest_times(m, b)
```

with uninitialized entries omitted. Thus:

- The rolling sample contains every arrival in the last `m` timesteps.
- The historical sample is exactly the existing `steady` algorithm applied
  to the prefix outside that rolling window. It has no overlap with the
  rolling sample and inherits steady's spacing guarantees.
- Once `T >= S`, there are exactly `m` samples of each kind. Before that,
  all received samples are retained.

The two halves are **logical groups**, not permanently separated address
ranges. Samples change groups by aging in place. As with ordinary `steady`,
historical spacing coarsens progressively and need not be identical between
every pair. Also, `steady` does not permanently retain the item at time zero;
the requirement here is coverage of the prefix starting at zero.

More precisely, let `delta = 2**max(0, bit_length(b)-s)`. Every completed
interval endpoint `delta-1, 2*delta-1, ...` below `b` is retained. Therefore
no run of missing historical arrivals, including the boundary at time zero
and the boundary with the rolling window, contains `delta` or more items.
For `b >= m`, `delta <= 2*b/m`. Additional retained samples can refine this
spacing. These coverage guarantees are tested directly on buffers maintained
by single-write replay, independently of the `steady` implementation.

For `S=16` and `T=64`, the policy retains:

```
historical:  3,  7, 15, 23, 31, 39, 47, 55
rolling:    56, 57, 58, 59, 60, 61, 62, 63
```

### Sampling every 2**n raw timesteps

The library algorithm assumes `n=0`: `T` counts sampled arrivals, not raw
clock ticks. For a raw-time spacing `d=2**n`, the caller ingests only at
raw times `0, d, 2d, ...`. Pass their consecutive sample indices `0, 1, 2, ...`
to the selector, and multiply reconstructed timestamps by `d`. After `R`
raw arrivals, the logical count for lookup is `(R+d-1)//d`.

```python
d = 4
surface = Surface(rolling_steady_algo, 16)
for raw_time in range(0, 256, d):
    surface.ingest_one(raw_time)
raw_timestamps = [None if t is None else t*d for t in surface.lookup()]
assert list(surface) == raw_timestamps
```

This retains the original policy's evenly spaced rolling sample on the raw
time grid without an algorithm configuration object or extra stream state.

## Derivation: overwrite chains

The delayed retention set determines exactly which sample must disappear
when a new sample arrives. It therefore determines disjoint chains of
samples that can share a physical slot.

Write `x = k+1 = o*2**h`, with `o` odd. Existing `steady(m)` accepts grid
sample `k` exactly when `o < m`. For an accepted sample, its physical segment
width is

```
w = s+1                         if o == 1
w = s+1 - bit_length(o)          otherwise
```

The next write to that steady slot has one-based index `2**w * x`.
Delaying archive ingestion by `m` arrivals therefore gives the following
successor on a physical overwrite chain:

```
G(x) = x + m                    if o >= m
G(x) = 2**w * x + m              if o < m
```

This is arithmetic on indices, **not a movement or delayed write of data**.
The arriving value is written directly into the slot computed for its chain.

There are exactly `2m` chains, starting at one-based indices `1, ..., 2m`:
the first `2m` samples fill the buffer, and every later arrival replaces
exactly one previously retained sample. A valid selector assigns a distinct,
time-independent label to each chain.

## Closed-form labels

### Permanent ring chains

If `x % m != 0` and its odd part is at least `m`, every successor is simply
`x + m`. Its nonzero residue `r = x % m` never changes. Give this chain slot

```
m + r                           # slots m+1, ..., 2m-1
```

### The other m+1 chains

For `x = m*y` with `y > m`, define

```
v = y - 1
e = floor(log2(v))
i = (v >> (e-s+1)) - m/2
C(i) = 2*i - popcount(i)
```

Give this chain slot

```
(e - C(i)) mod (m+1)             # slots 0, ..., m
```

The offsets `C(i) = 0,1,3,4,7,8,10,11,15,...` are
[OEIS A005187](https://oeis.org/A005187), the cumulative ruler function.
The OEIS identity supplies the constant-operation expression for the offsets;
the chain construction and its use as a selector are derived here.

To check invariance, consider a successor in terms of `y`:

- If steady rejects `y-1`, the successor is `y+1`. The top bits defining
  `(e,i)` do not change, because this increment does not cross a selected
  dyadic boundary.
- If `y=o*2**h` is accepted and `o>1`, the successor is `2**w*y+1`.
  Its `e` increases by `w`, and its mantissa index changes from `i-1` to `i`.
  The identity `C(i)-C(i-1) = 1+ctz(i) = w` preserves the label.
- If `y` is a power of two, the phase changes by exactly `m+1`, preserving
  the label modulo `m+1`.

For `1 <= y <= m`, one forward step reaches the preceding large-`y` case.
It need not actually be constructed. With `h=ctz(y)`, `o=y>>h`, set

```
i = (o << (s-bit_length(o))) - m/2
e = h + s + (o == 1)
```

and use the same phase formula.

### Reaching a labeled chain in at most two runs

The remaining case is `x % m != 0` with odd part `o < m`. While the
successor remains nondivisible by `m`, its valuation `h` increases and its
odd part increases. A run of `ell` steps with constant width `w` has the
closed form

```
G**ell(x) = 2**(ell*w)*x + m*(2**(ell*w)-1)/(2**w-1).
```

Let `b = bit_length(o)`, `p = s-h`, and `D = 2**w-1`. The run ends either
when the valuation reaches `s`, or when the odd part gains a binary digit:

```
ell_divisible = ceil(p / w)
B = 2**p - D*(2**b - o)
ell_carry = ceil((p - floor(log2(B))) / w)   if B > 0
ell = min(ell_divisible, ell_carry)         # omit carry if B <= 0
```

All quantities are evaluated with integer arithmetic. After this run the
chain is either already labeled, or its width has decreased by one. In the
latter case, one more geometric-series evaluation reaches a labeled chain.

Why only two runs? Before divisibility by `m`, each increase of the valuation
from `h` to `h+w` adds `2**(s-h-w)` to the odd part. All these increments
together, starting with width `w`, sum to less than
`2**(s-h-w+1) <= 2**b`. Therefore the odd part can gain at most one binary
digit. Width can change at most once. The special case `o=1` reaches
divisibility by `m` on its very first step.

This completes a finite expression for every arrival: at most two geometric
sums and one phase calculation. The selector contains no loops or recursion.

## Algebraic simplifications in the implementation

The derivation above describes the construction; the implementation uses
the following equivalent expressions, preserving the original slot numbers.

1. **Test permanent ring membership without a trailing-zero count.**
   For nonzero `r = x & (m-1)`, the least set bit `r & -r` is `2**h`.
   Consequently `odd_part(x) >= m` is equivalent to
   `(x >> s) >= (r & -r)`. This common path returns `m+r` without a
   trailing-zero count or multiplication. The quotient `x >> s` is also
   the normalized index needed when `r=0`.

2. **Combine the two stopping conditions into one division.**
   The carry threshold above always satisfies `B < 2**p`. Thus, if `B>0`,
   the carry stopping count cannot exceed the divisibility stopping count.
   Both cases reduce to

   ```
   ell = (p + w - bit_length(max(B, 1))) // w
   shift = ell*w
   ```

   `shift < p` identifies a carry before divisibility without another
   remainder operation. The new width is exactly `w-1`, and the remaining
   valuation distance is `p-shift`, so neither needs to be recomputed.
   If the original odd part already had `s` digits, this carry instead
   reaches a permanent ring chain. Its residue is
   `(r & ((m-1) >> shift)) << shift`: masking before shifting avoids
   constructing a larger intermediate. Return `m` plus that residue.

3. **Handle powers of two directly.** For `x=2**h < m`, the forward
   calculation gives `y=2*x+1`. Substitution into the phase formula reduces
   the final slot to

   ```
   (s + 1 - (m >> (h+1))) mod (m+1).
   ```

   This also covers `h=s-1`, where `y=m+1` crosses the phase branch boundary.
   The expression before modulo lies strictly between `-(m+1)` and `m+1`,
   so the implementation instead adds `m+1` only if it is negative.

4. **Use one additional leading bit in the phase calculation.** Define
   `a=m/2+i`. Since `a` has one more set bit than `i`,
   `C(a)=C(i)+m-1`. Therefore the same slot is

   ```
   (e - 2*a + popcount(a) - 2) mod (m+1).
   ```

   Now choose `z` with `a=z//2`. Whether `z` is odd or even,
   `2*a-popcount(a) = z-popcount(z)`, eliminating the doubling:

   ```
   slot = (e - z + popcount(z) - 2) mod (m+1)
   ```

   For large `y`, take the top `s+1` bits of `y-1`:
   `z=(y-1) >> (e-s)`. For small `y`, left-normalize to `s+1` bits:
   `z=y << (s+1-bit_length(y))`. This uses only one shift and the shift
   count is nonnegative, including at `y=m`.

5. **Eliminate the virtual forward indices entirely.** Work with the
   odd part `o` and remaining valuation distance `p=s-h`. If a carry
   occurs after total shift `L<p`, the new odd part is

   ```
   o' = o + (2**p - 2**(p-L))/D
      = 2**b + (B - 2**(p-L))/D.
   ```

   The second expression reuses the already computed carry threshold
   `B=2**p-D*(2**b-o)`. Set `p'=p-L`, `w'=w-1`, and `D'=D>>1`.
   There is no need to construct `G**ell(x)` or calculate its odd part
   again. If there is no carry, keep the original `o,p,w,D`.

   In either case the final shift is `L=w*ceil(p/w)`. Compute the final
   normalized index directly:

   ```
   y = o*2**(L-p) + (2**L-1)/D.
   ```

   Only this final geometric sum remains. To avoid its potentially large
   numerator, let `head=2**(L-w)` and use the identity

   ```
   (2**L-1)/D = head + (head-1)/D
   y = (o << (L-p)) + head + (head-1)//D.
   ```

   Both divisions shown in this point are exact. Since `L-w<p` and
   `bit_length(o)+w=s+1`, `head <= m/2`, the shifted odd part is less
   than `m`, and the geometric sum is less than `m`. Consequently this
   warm-up branch produces `y<2m`, without constructing indices of
   order `m**2`.

## Startup paths and remaining divisions

The nonzero-residue path after the permanent-ring check is used only when
`odd_part(x) < m` and `ctz(x) < s`. Consequently
`x <= (m-1)*(m/2) < m*m/2`. Its geometric-run calculations and all `//`
operations in the selector disappear before that bound. The `y <= m` phase
normalization is also an early-time path, absent once `T >= m*m`. These
startup paths can still run after the buffer first fills at `T=S`.

After `T >= m*m`, selection uses only the permanent-ring return or the
large-`y` phase calculation. The remaining modulo is by `m+1`, a non-power
of two. The early-time divisors `w` and `2**w-1` are also not generally powers
of two. Replacing these operations with single shifts or masks would give
incorrect labels; synthesizing division with reciprocal construction or
iterated bit folding would add machinery. The implementation keeps these
operations explicit, uses a right shift for division by two, and replaces
the bounded power-of-two branch's modulo with a conditional addition.

## Why the labels cannot collide

The label is invariant along every overwrite chain. Every chain reaches
one of the two labeled cases above. All `m-1` ring labels occur, and all
`m+1` phase labels occur: take `y = 2**e+1` for successive sufficiently
large `e`, which gives phase `e mod (m+1)`.

There are exactly `2m` chains and exactly `2m` realized labels. Thus the
labeling is a bijection. Writing each arriving payload at its chain label
implements precisely the required retention set, with one write and no
relocation.

## Lookup, complexity, and validation

Timestamp lookup generates the specified retained set using ordinary
`steady` lookup and the rolling interval, then applies the selector to
each timestamp to recover its physical slot. This costs `O(S)` word
operations and produces `S` timestamps. The output is not persistent metadata.

Selection is `O(1)` in the word-RAM model with word-sized shifts, arithmetic,
division/remainder, bit length, and population count. It uses a fixed number
of temporary scalar values and no precomputed tables. Python uses a constant
number of arbitrary-precision operations, not constant bit complexity.
Compiled ports must provide sufficient width for `k+1`. Apart from the
supplied stream index and its quotient, the warm-up arithmetic now uses
values bounded by `S`; it does not require squared-capacity intermediates.
Phase arithmetic uses signed expressions and mathematical nonnegative
remainders. Batched selection and lookup currently use serial scalar
fallbacks; the lookup `parallel` argument is accepted for API compatibility.

Run the independent replay and boundary checks from the repository root:

```
python -m pytest -q test_downstream/test_dstream/test_rolling_steady_algo
```

The tests check every retained payload against a separately advanced
`steady` buffer; timestamp reconstruction; full occupancy; exact separation
of the two time periods; direct coverage and maximum-gap bounds including
both historical edges; caller-side raw-time sampling; and large integer
cases up to 256-bit arrival indices. API checks cover module exports,
capacity, batched broadcasting, lookup variants, and uint64 boundaries.

Context: the single-write/no-relocation model and existing steady algorithm
are described in [Yang et al., Downstream](https://arxiv.org/abs/2506.12975)
and [Moreno et al., Structured Downsampling](https://arxiv.org/abs/2409.06199).
