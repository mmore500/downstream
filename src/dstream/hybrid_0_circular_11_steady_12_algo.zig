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
    if (S < 12 or S % 12 != 0) {
        return false;
    }
    const twelfth_S = S / 12;
    const eleven_twelfth_S = 11 * twelfth_S;
    const T_div_12 = T / 12;
    const T_mod_12 = T % 12;
    const adj_T_mod: u = if (T_mod_12 < 11) T_mod_12 else 10;
    const has_capacity_1st = circular_algo.has_ingest_capacity(
        u,
        eleven_twelfth_S,
        T_div_12 * 11 + adj_T_mod,
    );
    const has_capacity_2nd = ((T < 11) or steady_algo.has_ingest_capacity(
        u,
        twelfth_S,
        (T - 11) / 12,
    ));
    return has_capacity_1st and has_capacity_2nd;
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 12, with S/12 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    const twelfth_S = S / 12;
    const eleven_twelfth_S = 11 * twelfth_S;
    const remainder = T % 12;
    if (remainder < 11) {
        const adj_T = (T / 12) * 11 + remainder;
        const site = circular_algo.assign_storage_site(u, eleven_twelfth_S, adj_T);
        return if (site == eleven_twelfth_S) S else site;
    } else {
        const adj_T = T / 12;
        const site = steady_algo.assign_storage_site(u, twelfth_S, adj_T);
        return if (site == twelfth_S) S else eleven_twelfth_S + site;
    }
}
