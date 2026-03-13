const std = @import("std");

const aux = @import("../_auxlib.zig");

const steady_algo = @import("./steady_algo.zig");
const tilted_algo = @import("./tilted_algo.zig");

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
pub fn has_ingest_capacity(comptime u: type, S: u, T: u) bool {
    aux.assert_unsigned(u);
    if (S < 3 or S % 3 != 0) {
        return false;
    }
    const third_S = S / 3;
    const two_thirds_S = 2 * third_S;
    const T_div_3 = T / 3;
    const has_capacity_1st = steady_algo.has_ingest_capacity(
        u,
        two_thirds_S,
        T_div_3 * 2 + @intFromBool(T % 3 > 0),
    );
    const has_capacity_2nd = ((T < 2) or tilted_algo.has_ingest_capacity(
        u,
        third_S,
        (T - 2) / 3,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

/// Site selection for hybrid steady/tilted curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 3, with S/3 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const third_S = S / 3;
    const two_thirds_S = 2 * third_S;
    const remainder = T % 3;
    if (remainder < 2) {
        const adj_T = (T / 3) * 2 + remainder;
        const site = steady_algo.assign_storage_site(u, two_thirds_S, adj_T);
        return if (site == two_thirds_S) S else site;
    } else {
        const adj_T = T / 3;
        const site = tilted_algo.assign_storage_site(u, third_S, adj_T);
        return if (site == third_S) S else two_thirds_S + site;
    }
}
