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
    if (S < 8 or S % 8 != 0) {
        return false;
    }
    const eighth_S = S / 8;
    const seven_eighth_S = 7 * eighth_S;
    const T_div_8 = T / 8;
    const T_mod_8 = T % 8;
    const adj_T_mod: u = if (T_mod_8 < 7) T_mod_8 else 6;
    const has_capacity_1st = circular_algo.has_ingest_capacity(
        u,
        seven_eighth_S,
        T_div_8 * 7 + adj_T_mod,
    );
    const has_capacity_2nd = ((T < 7) or steady_algo.has_ingest_capacity(
        u,
        eighth_S,
        (T - 7) / 8,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 8, with S/8 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const eighth_S = S / 8;
    const seven_eighth_S = 7 * eighth_S;
    const remainder = T % 8;
    if (remainder < 7) {
        const adj_T = (T / 8) * 7 + remainder;
        const site = circular_algo.assign_storage_site(u, seven_eighth_S, adj_T);
        return if (site == seven_eighth_S) S else site;
    } else {
        const adj_T = T / 8;
        const site = steady_algo.assign_storage_site(u, eighth_S, adj_T);
        return if (site == eighth_S) S else seven_eighth_S + site;
    }
}
