const std = @import("std");

const aux = @import("../_auxlib.zig");

pub fn has_ingest_capacity(S: u32, T: u32) bool {
    const surface_size_ok = S > 1 and (@popCount(S) == 1);
    if (!surface_size_ok) {
        return false;
    }
    if (S >= @bitSizeOf(u32)) {
        return true;
    }

    const one: u32 = 1;
    const ingest_capacity = (one << @intCast(S)) - 1;
    return T < ingest_capacity;
}

pub fn assign_storage_site(S: u32, T: u32) u32 {
    std.debug.assert(has_ingest_capacity(S, T));

    const s = aux.bit_length(S) - 1;
    const t = aux.floor_subtract(aux.bit_length(T), s); // Current epoch
    const h = @ctz(T + 1); // Current hanoi value
    const i = T >> @intCast(h + 1); // Hanoi value incidence (i.e., num seen)

    const blt = aux.bit_length(t); // Bit length of t
    const epsilon_tau: u32 = @intFromBool(aux.bit_floor(t << 1) > t + blt);
    // ^^^ Correction factor
    const tau = blt - epsilon_tau; // Current meta-epoch
    const one: u32 = 1;
    const t_0 = (one << @intCast(tau)) - tau; // Opening epoch of meta-epoch
    const t_1 = (one << @intCast(tau + 1)) - (tau + 1);
    // ^^^ Opening epoch of next meta-epoch
    const epsilon_b: u32 = @intFromBool(t < h + t_0 and h + t_0 < t_1);
    // ^^^ uninvaded correction factor
    const B = @max(S >> @intCast(tau + 1 - epsilon_b), 1);
    // ^^^ Num bunches available to h.v.

    const b_l = aux.modpow2(i, B); // Logical bunch index...
    // ... i.e., in order filled (increasing nestedness/decreasing init size r)

    // Need to calculate physical bunch index...
    // ... i.e., position among bunches left-to-right in buffer space
    const v = aux.bit_length(b_l);
    // ^^^ Nestedness depth level of physical bunch
    const w = (S >> @intCast(v)) * @intFromBool(v > 0);
    // ^^^ Num bunches spaced between bunches in nest level
    const o = w >> 1; // Offset of nestedness level in physical bunch order
    const p = b_l - aux.bit_floor(b_l);
    // ^^^ Bunch position within nestedness level
    const b_p = o + w * p; // Physical bunch index...
    // ... i.e., in left-to-right sequential bunch order

    // Need to calculate buffer position of b_p'th bunch
    const epsilon_k_b = @intFromBool(b_l > 0);
    // ^^^ Correction factor for zeroth bunch...
    // ... i.e., bunch r=s at site k=0
    const k_b = ( // Site index of bunch
        (b_p << 1) + @popCount((S << 1) - b_p) -% 1 -% epsilon_k_b);

    return k_b + h; // Calculate placement site, h.v. h is offset within bunch

}