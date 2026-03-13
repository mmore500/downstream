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

/// Site selection implementation for circular curation.
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
    T % S
}

/// Site selection implementation for circular curation.
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
