const std = @import("std");

const aux = @import("../_auxlib.zig");

const steady_algo = @import("./steady_algo.zig");
const stretched_algo = @import("./stretched_algo.zig");

pub fn has_ingest_capacity(comptime u: type, S: u, T: u) bool {
    aux.assert_unsigned(u);
    const half_S = S >> 1;
    const has_capacity_1st = steady_algo.has_ingest_capacity(
        u,
        half_S,
        T >> 1,
    );
    const has_capacity_2nd = ((T == 0) or stretched_algo.has_ingest_capacity(
        u,
        half_S,
        (T - 1) >> 1,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const half_S = S >> 1;
    const half_T = T >> 1;
    if (T & 1 == 0) {
        const site = steady_algo.assign_storage_site(u, half_S, half_T);
        return if (site == half_S) S else site;
    } else {
        return half_S + stretched_algo.assign_storage_site(u, half_S, half_T);
    }
}
