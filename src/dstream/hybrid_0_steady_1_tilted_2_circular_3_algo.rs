use super::{AssignStorageSiteTrait, CircularAlgo, HasIngestCapacityTrait, SteadyAlgo, TiltedAlgo};
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
    let _0: Uint = Uint::zero();
    let _1: Uint = Uint::one();
    let _2: Uint = _1 + _1;
    let _3: Uint = _2 + _1;
    if S < _3 || S % _3 != _0 {
        return false;
    }
    let third_S: Uint = S / _3;
    let has_capacity_1st = SteadyAlgo::has_ingest_capacity(third_S, T / _3);
    let has_capacity_2nd = T < _1 || TiltedAlgo::has_ingest_capacity(third_S, (T - _1) / _3);
    let has_capacity_3rd = T < _2 || CircularAlgo::has_ingest_capacity(third_S, (T - _2) / _3);

    has_capacity_1st && has_capacity_2nd && has_capacity_3rd
}

/// Site selection for hybrid steady/tilted/circular curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 3, with S/3 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn _assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    debug_assert!(has_ingest_capacity(S, T));

    let _0: Uint = Uint::zero();
    let _1: Uint = Uint::one();
    let _2: Uint = _1 + _1;
    let _3: Uint = _2 + _1;
    let third_S: Uint = S / _3;
    let adj_T: Uint = T / _3;
    let remainder: Uint = T % _3;
    if remainder == _0 {
        let site: Uint = SteadyAlgo::_assign_storage_site(third_S, adj_T);
        if site == third_S {
            S
        } else {
            site
        }
    } else if remainder == _1 {
        let site: Uint = TiltedAlgo::_assign_storage_site(third_S, adj_T);
        if site == third_S {
            S
        } else {
            third_S + site
        }
    } else {
        let site: Uint = CircularAlgo::_assign_storage_site(third_S, adj_T);
        if site == third_S {
            S
        } else {
            _2 * third_S + site
        }
    }
}

/// Site selection for hybrid steady/tilted/circular curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 3, with S/3 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns None if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Option<Uint> {
    let k: Uint = _assign_storage_site(S, T);
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
        has_ingest_capacity::<u32>(12, 5);
    }

    #[test]
    fn test_smoke_assign_storage_site() {
        assign_storage_site::<u32>(12, 5);
    }

    #[test]
    fn test_smoke_impl_assign_storage_site() {
        _assign_storage_site::<u32>(12, 5);
    }
}
