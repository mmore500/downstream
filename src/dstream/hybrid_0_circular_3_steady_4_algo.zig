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
    if (S < 4 or S % 4 != 0) {
        return false;
    }
    const quarter_S = S / 4;
    const three_quarter_S = 3 * quarter_S;
    const T_div_4 = T / 4;
    const T_mod_4 = T % 4;
    const adj_T_mod: u = if (T_mod_4 < 3) T_mod_4 else 2;
    const has_capacity_1st = circular_algo.has_ingest_capacity(
        u,
        three_quarter_S,
        T_div_4 * 3 + adj_T_mod,
    );
    const has_capacity_2nd = ((T < 3) or steady_algo.has_ingest_capacity(
        u,
        quarter_S,
        (T - 3) / 4,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 4, with S/4 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const quarter_S = S / 4;
    const three_quarter_S = 3 * quarter_S;
    const remainder = T % 4;
    if (remainder < 3) {
        const adj_T = (T / 4) * 3 + remainder;
        const site = circular_algo.assign_storage_site(u, three_quarter_S, adj_T);
        return if (site == three_quarter_S) S else site;
    } else {
        const adj_T = T / 4;
        const site = steady_algo.assign_storage_site(u, quarter_S, adj_T);
        return if (site == quarter_S) S else three_quarter_S + site;
    }
}
