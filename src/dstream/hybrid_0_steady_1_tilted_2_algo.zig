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
    const half_S = S >> 1;
    const has_capacity_1st = steady_algo.has_ingest_capacity(
        u,
        half_S,
        T >> 1,
    );
    const has_capacity_2nd = ((T == 0) or tilted_algo.has_ingest_capacity(
        u,
        half_S,
        (T - 1) >> 1,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

/// Site selection for hybrid steady/tilted curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be a power of two, greater than 2.
/// @param T Current logical time.
///    Must be less than 2^(S - 1) - 1.
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const half_S = S >> 1;
    const half_T = T >> 1;
    if (T & 1 == 0) {
        const site = steady_algo.assign_storage_site(u, half_S, half_T);
        return if (site == half_S) S else site;
    } else {
        return half_S + tilted_algo.assign_storage_site(u, half_S, half_T);
    }
}
