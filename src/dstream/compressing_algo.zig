const std = @import("std");

const aux = @import("../_auxlib.zig");

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
pub fn has_ingest_capacity(comptime u: type, S: u, T: u) bool {
    aux.assert_unsigned(u);
    _ = T;
    return S > 0;
}

/// Site selection for compressing curation with even buffer size.
///
/// Site 0 is special (always holds T=0). Remaining S-1 sites are managed
/// with modulus M = S - 1.
fn assign_storage_site_even_S(comptime u: type, S: u, T: u) u {
    std.debug.assert(S & 1 == 0);

    if (T == 0) return 0;

    const M = S - 1;
    const T_ = T - 1;
    const si = aux.bit_length(u, T_ / M); // Current sampling interval
    const h: u = @ctz(@max(T_, 1)); // Hanoi value
    if (h < si) // discard without storing
        return S
    else
        return T_ % M + 1;
}

/// Site selection for compressing curation with odd buffer size.
///
/// No special site. All S sites participate uniformly with modulus M = S.
fn assign_storage_site_odd_S(comptime u: type, S: u, T: u) u {
    std.debug.assert(S & 1 == 1);

    const M = S;
    const si = aux.bit_length(u, T / M); // Current sampling interval
    const h: u = @ctz(@max(T, 1)); // Hanoi value
    if (h < si) // discard without storing
        return S
    else
        return T % M;
}

/// Site selection for compressing curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @param u Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be greater than 0.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
pub fn assign_storage_site(comptime u: type, S: u, T: u) u {
    aux.assert_unsigned(u);
    std.debug.assert(has_ingest_capacity(u, S, T));

    return if (S & 1 == 0)
        assign_storage_site_even_S(u, S, T)
    else
        assign_storage_site_odd_S(u, S, T);
}
