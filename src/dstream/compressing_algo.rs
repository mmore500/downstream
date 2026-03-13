use crate::_auxlib as aux;

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @template Uint Unsigned integer type for operands.
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
#[allow(non_snake_case)]
pub fn has_ingest_capacity<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> bool {
    _ = T;
    S > Uint::zero()
}

/// Site selection for compressing curation with even buffer size.
///
/// Site 0 is special (always holds T=0). Remaining S-1 sites are managed
/// with modulus M = S - 1.
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size. Must be positive and even.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
fn _assign_storage_site_even_s<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    let _0: Uint = Uint::zero();
    let _1: Uint = Uint::one();

    if T == _0 {
        return _0;
    }

    let m: Uint = S - _1;
    let t_: Uint = T - _1;
    let si: Uint = aux::bit_length::<Uint>(t_ / m); // Current sampling interval
    let h: Uint = aux::ctz::<Uint>(std::cmp::max(t_, _1)); // Hanoi value
    if h < si {
        S // discard without storing
    } else {
        t_ % m + _1
    }
}

/// Site selection for compressing curation with odd buffer size.
///
/// No special site. All S sites participate uniformly with modulus M = S.
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size. Must be positive and odd.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
fn _assign_storage_site_odd_s<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    let _1: Uint = Uint::one();

    let m: Uint = S;
    let si: Uint = aux::bit_length::<Uint>(T / m); // Current sampling interval
    let h: Uint = aux::ctz::<Uint>(std::cmp::max(T, _1)); // Hanoi value
    if h < si {
        S // discard without storing
    } else {
        T % m
    }
}

/// Site selection implementation for compressing curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be greater than 0.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn _assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    debug_assert!(has_ingest_capacity(S, T));
    let _1: Uint = Uint::one();

    if S & _1 == Uint::zero() {
        _assign_storage_site_even_s::<Uint>(S, T)
    } else {
        _assign_storage_site_odd_s::<Uint>(S, T)
    }
}

/// Site selection implementation for compressing curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be greater than 0.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns None if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Option<Uint> {
    let k = _assign_storage_site(S, T);
    if k == S {
        None
    } else {
        Some(k)
    }
}

pub struct Algo;

#[allow(non_snake_case)]
impl crate::dstream::HasIngestCapacityTrait for Algo {
    fn has_ingest_capacity<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> bool {
        has_ingest_capacity::<Uint>(S, T)
    }
}

#[allow(non_snake_case)]
impl crate::dstream::AssignStorageSiteTrait for Algo {
    fn _assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
        _assign_storage_site::<Uint>(S, T)
    }

    fn assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Option<Uint> {
        assign_storage_site::<Uint>(S, T)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_smoke_has_ingest_capacity() {
        has_ingest_capacity::<u32>(16, 101);
    }

    #[test]
    fn test_smoke_impl_assign_storage_site() {
        _assign_storage_site::<u32>(16, 101);
    }

    #[test]
    fn test_smoke_assign_storage_site() {
        assign_storage_site::<u32>(16, 101);
    }
}
