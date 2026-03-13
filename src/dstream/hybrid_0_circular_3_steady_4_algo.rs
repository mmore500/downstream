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
    let _3: Uint = _2 + _1;
    let _4: Uint = _3 + _1;
    if S < _4 || S % _4 != _0 {
        return false;
    }
    let quarter_S: Uint = S / _4;
    let three_quarter_S: Uint = _3 * quarter_S;
    let t_div_4: Uint = T / _4;
    let t_mod_4: Uint = T % _4;
    let adj_t_mod: Uint = if t_mod_4 < _3 { t_mod_4 } else { _2 };
    let has_capacity_1st =
        CircularAlgo::has_ingest_capacity(three_quarter_S, t_div_4 * _3 + adj_t_mod);
    let has_capacity_2nd = T < _3 || SteadyAlgo::has_ingest_capacity(quarter_S, (T - _3) / _4);

    has_capacity_1st && has_capacity_2nd
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 4, with S/4 being a power of two.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn _assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    debug_assert!(has_ingest_capacity(S, T));

    let _1: Uint = Uint::one();
    let _2: Uint = _1 + _1;
    let _3: Uint = _2 + _1;
    let _4: Uint = _3 + _1;
    let quarter_S: Uint = S / _4;
    let three_quarter_S: Uint = _3 * quarter_S;
    let remainder: Uint = T % _4;
    if remainder < _3 {
        let adj_T: Uint = (T / _4) * _3 + remainder;
        let site: Uint = CircularAlgo::_assign_storage_site(three_quarter_S, adj_T);
        if site == three_quarter_S {
            S
        } else {
            site
        }
    } else {
        let adj_T: Uint = T / _4;
        let site: Uint = SteadyAlgo::_assign_storage_site(quarter_S, adj_T);
        if site == quarter_S {
            S
        } else {
            three_quarter_S + site
        }
    }
}

/// Site selection for hybrid circular/steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be divisible by 4, with S/4 being a power of two.
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
        has_ingest_capacity::<u32>(16, 5);
    }

    #[test]
    fn test_smoke_assign_storage_site() {
        assign_storage_site::<u32>(16, 5);
    }

    #[test]
    fn test_smoke_impl_assign_storage_site() {
        _assign_storage_site::<u32>(16, 5);
    }
}
