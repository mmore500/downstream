const std = @import("std");

const aux = @import("../_auxlib.zig");

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
pub fn has_ingest_capacity(comptime u: type, S: u, T: u) bool {
    aux.assert_unsigned(u);

    _ = T;
    return (@popCount(S) == 1) and S > 1;
}

/// Site selection for steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be a power of two greater than 1.
/// @param T Current logical time.
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const s = aux.bit_length(u, S) - 1;
    const blT = aux.bit_length(u, T);
    const t = aux.floor_subtract(u, blT, s); // Current epoch
    const h = @ctz(T +% 1); // Current hanoi value

    // Hanoi value incidence (i.e., num seen)
    const i = aux.overflow_shr(u, T, h + 1);

    // Num full-bunch segments
    const j = aux.bit_floor(u, i) -% 1;
    const B = aux.bit_length(u, j); // Num full bunches
    // Bunch position
    var k_b = aux.overflow_shl(u, 1, B) *% (s + 1 -% B);
    // substituting t = s - blT into h + 1 - t
    var w = h + s + 1 -% blT; // Segment width
    var o = w *% (i -% (j +% 1)); // Within-bunch offset

    const is_zeroth_bunch = i == 0;
    k_b = if (!is_zeroth_bunch) k_b else 0;
    o = if (!is_zeroth_bunch) o else 0;
    w = if (!is_zeroth_bunch) w else s + 1;

    std.debug.assert(w > 0 or h < t); // ensure no divide-by-zero

    // handle discard without storing for non-top n(T) hanoi value...
    return if (h >= t) k_b + o + (h % w) else S;
    // within-segment offset: p  ^^^%^^^
}
