const std = @import("std");

const aux = @import("../_auxlib.zig");

const circular_algo = @import("./circular_algo.zig");
const steady_algo = @import("./steady_algo.zig");

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
pub fn has_ingest_capacity(comptime u: type, S: u, T: u) bool {
    aux.assert_unsigned(u);
    if (S < 6 or S % 6 != 0) {
        return false;
    }
    const sixth_S = S / 6;
    const five_sixth_S = 5 * sixth_S;
    const T_div_6 = T / 6;
    const T_mod_6 = T % 6;
    const adj_T_mod: u = if (T_mod_6 < 5) T_mod_6 else 4;
    const has_capacity_1st = circular_algo.has_ingest_capacity(
        u,
        five_sixth_S,
        T_div_6 * 5 + adj_T_mod,
    );
    const has_capacity_2nd = ((T < 5) or steady_algo.has_ingest_capacity(
        u,
        sixth_S,
        (T - 5) / 6,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 6, with S/6 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const sixth_S = S / 6;
    const five_sixth_S = 5 * sixth_S;
    const remainder = T % 6;
    if (remainder < 5) {
        const adj_T = (T / 6) * 5 + remainder;
        const site = circular_algo.assign_storage_site(u, five_sixth_S, adj_T);
        return if (site == five_sixth_S) S else site;
    } else {
        const adj_T = T / 6;
        const site = steady_algo.assign_storage_site(u, sixth_S, adj_T);
        return if (site == sixth_S) S else five_sixth_S + site;
    }
}
