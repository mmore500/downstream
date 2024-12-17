const std = @import("std");

const aux = @import("../_auxlib.zig");

pub fn has_ingest_capacity(S: u64, T: u64) bool {
    _ = T;
    return (@popCount(S) == 1) and S > 1;
}

pub fn assign_storage_site(S: u64, T: u64) u64 {
    const s = aux.bit_length(S) - 1;
    const blt = aux.bit_length(T);
    const t = aux.floor_subtract(blt, s); // Current epoch
    const h = @ctz(T + 1); // Current hanoi value

    // Hanoi value incidence (i.e., num seen)
    const i = T >> @intCast(h + 1);

    // Num full-bunch segments
    const j = aux.floor_subtract(aux.bit_floor(i), 1);
    const B = aux.bit_length(j); // Num full bunches
    const one: u64 = 1;
    // Bunch position
    var k_b = (one << @intCast(B)) * aux.floor_subtract(s + 1, B);
    var w = aux.floor_subtract(h + s + 1, blt); // Segment width
    var o = w * aux.floor_subtract(i, j + 1); // Within-bunch offset

    const is_zeroth_bunch = i == 0;
    k_b = if (!is_zeroth_bunch) k_b else 0;
    o = if (!is_zeroth_bunch) o else 0;
    w = if (!is_zeroth_bunch) w else s + 1;

    const p = h % @max(w, 1); // Within-segment offset, avoiding divide by zero

    // handle discard without storing for non-top n(T) hanoi value...
    return if (h >= t) k_b + o + p else S;
}
