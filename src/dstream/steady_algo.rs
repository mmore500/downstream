use crate::_auxlib as aux;

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @template UInt Unsigned integer type for operands.
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
#[allow(non_snake_case)]
pub fn has_ingest_capacity<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> bool {
    _ = T;
    (S.count_ones() == 1) && S > Uint::one()
}

/// Site selection implementation for steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template UInt Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be a power of two greater than 1.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn _assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Uint {
    debug_assert!(has_ingest_capacity(S, T));
    let _0: Uint = Uint::zero();
    let _1: Uint = Uint::one();

    let s: Uint = aux::bit_length::<Uint>(S) - _1;
    let blT: Uint = aux::bit_length::<Uint>(T);
    let t: Uint = aux::floor_subtract::<Uint>(blT, s); // Current epoch
    let h: Uint = aux::ctz::<Uint>(T.wrapping_add(&_1)); // Current hanoi value

    // Hanoi value incidence (i.e., num seen)
    let i: Uint = aux::overflow_shr::<Uint>(T, h + _1);

    // Num full-bunch segments
    let j: Uint = aux::bit_floor::<Uint>(i).wrapping_sub(&_1);
    let B: Uint = aux::bit_length::<Uint>(j); // Num full bunches
                                              // Bunch position
    let mut k_b: Uint = aux::overflow_shl::<Uint>(_1, B).wrapping_mul(&(s + _1).wrapping_sub(&B));
    // substituting t = s - blT into h + 1 - t
    let mut w: Uint = (h + s + _1).wrapping_sub(&blT); // Segment width
    let mut o: Uint = w.wrapping_mul(&i.wrapping_sub(&j.wrapping_add(&_1))); // Within-bunch offset

    let is_zeroth_bunch = i == _0;
    k_b = if !is_zeroth_bunch { k_b } else { _0 };
    o = if !is_zeroth_bunch { o } else { _0 };
    w = if !is_zeroth_bunch { w } else { s + _1 };

    debug_assert!(w > _0 || h < t); // ensure no divide-by-zero

    // handle discard without storing for non-top n(T) hanoi value...
    if h >= t {
        k_b + o + (h % w)
    } else {
        S
    }
    // within-segment offset: p  ^^^%^^^
}

/// Site selection implementation for steady curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template UInt Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be a power of two greater than 1.
/// @param T Current logical time.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn assign_storage_site<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> Option<Uint> {
    let k = _assign_storage_site(S, T);
    if k == S { None } else { Some(k) }
}

pub struct SteadyAlgo;

#[allow(non_snake_case)]
impl crate::dstream::HasIngestCapacityTrait for SteadyAlgo {
    fn has_ingest_capacity<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> bool {
        has_ingest_capacity::<Uint>(S, T)
    }
}

#[allow(non_snake_case)]
impl crate::dstream::AssignStorageSiteTrait for SteadyAlgo {
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
