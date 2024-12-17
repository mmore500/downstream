const std = @import("std");

const aux = @import("../_auxlib.zig");

pub fn has_ingest_capacity(S: u64, T: u64) bool {
    _ = T;
    return (@popCount(S) == 1) and S > 1;
}

pub fn assign_storage_site(S: u64, T: u64) u64 {
    const s = aux.bit_length(S) - 1;
    const blt = aux.bit_length(T);
    const t = blt - @min(s, blt); // Current epoch (or negative)
    const h = @ctz(T + 1); // Current hanoi value

    // If not a top n(T) hanoi value, discard without storing
    if (h < t) { return S; }

    // Hanoi value incidence (i.e., num seen)
    const i = T >> @intCast(h + 1);

    var k_b: u64 = 0;
    var o: u64 = 0;
    var w: u64 = 0;

    if (i == 0) {
        // Special case the 0th bunch
        k_b = 0; // Bunch position
        o = 0; // Within-bunch offset
        w = s + 1; // Segment width
    } else {
        const j = aux.bit_floor(i) - 1; // Num full-bunch segments
        const B = aux.bit_length(j); // Num full bunches

        // Bunch position:
        k_b = ((@as(u64, 1) << @intCast(B)) * (s - B + 1));

        if (h + 1 <= t) { return S; } // if w <= 0
        w = h - t + 1; // Segment width
        o = w * (i - j - 1); // Within-bunch offset
    }

    const p = h % w; // Within-segment offset
    return (k_b + o) + p;
}
