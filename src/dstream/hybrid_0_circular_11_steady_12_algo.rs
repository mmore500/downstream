use super::{AssignStorageSiteTrait, CircularAlgo, HasIngestCapacityTrait, SteadyAlgo};
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
    let _4: Uint = _2 + _2;
    let _8: Uint = _4 + _4;
    let _10: Uint = _8 + _2;
    let _11: Uint = _8 + _2 + _1;
    let _12: Uint = _8 + _4;
    if S < _12 || S % _12 != _0 {
        return false;
    }
    let twelfth_S: Uint = S / _12;
    let eleven_twelfth_S: Uint = _11 * twelfth_S;
    let t_div_12: Uint = T / _12;
    let t_mod_12: Uint = T % _12;
    let adj_t_mod: Uint = if t_mod_12 < _11 { t_mod_12 } else { _10 };
    let has_capacity_1st =
        CircularAlgo::has_ingest_capacity(eleven_twelfth_S, t_div_12 * _11 + adj_t_mod);
    let has_capacity_2nd = T < _11 || SteadyAlgo::has_ingest_capacity(twelfth_S, (T - _11) / _12);

    has_capacity_1st && has_capacity_2nd
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 12, with S/12 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn _assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    debug_assert!(has_ingest_capacity(S, T));

    let _1: Uint = Uint::one();
    let _2: Uint = _1 + _1;
    let _4: Uint = _2 + _2;
    let _8: Uint = _4 + _4;
    let _11: Uint = _8 + _2 + _1;
    let _12: Uint = _8 + _4;
    let twelfth_S: Uint = S / _12;
    let eleven_twelfth_S: Uint = _11 * twelfth_S;
    let remainder: Uint = T % _12;
    if remainder < _11 {
        let adj_T: Uint = (T / _12) * _11 + remainder;
        let site: Uint = CircularAlgo::_assign_storage_site(eleven_twelfth_S, adj_T);
        if site == eleven_twelfth_S {
            S
        } else {
            site
        }
    } else {
        let adj_T: Uint = T / _12;
        let site: Uint = SteadyAlgo::_assign_storage_site(twelfth_S, adj_T);
        if site == twelfth_S {
            S
        } else {
            eleven_twelfth_S + site
        }
    }
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 12, with S/12 being a power of two.
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
        has_ingest_capacity::<u32>(24, 5);
    }

    #[test]
    fn test_smoke_assign_storage_site() {
        assign_storage_site::<u32>(24, 5);
    }

    #[test]
    fn test_smoke_impl_assign_storage_site() {
        _assign_storage_site::<u32>(24, 5);
    }
}
