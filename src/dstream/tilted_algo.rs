use crate::_auxlib as aux;

/// Does this algorithm have the capacity to ingest a data item at logical time
/// T?
///
/// @template Uint Unsigned integer type for operands.
/// @param S The number of buffer sites available.
/// @param T Queried logical time.
/// @returns Whether there is capacity to ingest at time T.
#[allow(non_snake_case, clippy::just_underscores_and_digits)]
pub fn has_ingest_capacity<Uint: aux::UnsignedTrait>(S: Uint, T: Uint) -> bool {
    let _0: Uint = Uint::zero();
    let _1: Uint = Uint::one();

    let surface_size_ok: bool = S > _1 && (S.count_ones() == 1);
    let overflow_epsilon: Uint = aux::from_bool::<Uint>(
        T.wrapping_add(&_1) < T, // nofmt
    );

    surface_size_ok
        && (_0
            == aux::overflow_shr::<Uint>(
                (T - overflow_epsilon) + _1, // nofmt
                S - overflow_epsilon,        // nofmt
            ))
}

/// Site selection implementation for tilted curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be a power of two greater than 1, and 2 * S must not overflow Uint.
/// @param T Current logical time.
///     Must be less than 2^S - 1.
/// @returns The selected storage site, if any.
///     Returns S if no site should be selected (i.e., discard).
#[allow(non_snake_case, clippy::just_underscores_and_digits)]
pub fn _assign_storage_site<Uint: aux::UnsignedTrait>(
    S: Uint, // nofmt
    T: Uint, // nofmt
) -> Uint {
    let _0: Uint = Uint::zero();
    let _1: Uint = Uint::one();
    debug_assert!(aux::clz(S) >= _1); // otherwise, calculations overflow
    debug_assert!(has_ingest_capacity(S, T));

    let s: Uint = aux::bit_length::<Uint>(S) - _1;
    let t: Uint = aux::floor_subtract::<Uint>(
        aux::bit_length::<Uint>(T), // nofmt
        s,                          // nofmt
    );
    // ^^^ Current epoch
    let h: Uint = aux::ctz::<Uint>(T.wrapping_add(&_1)); // Current hanoi value
    let i: Uint = aux::overflow_shr::<Uint>(T, h + _1);
    // ^^^ Hanoi value incidence (i.e., num seen)

    let blt: Uint = aux::bit_length::<Uint>(t); // Bit length of t
    let epsilon_tau: Uint = aux::from_bool::<Uint>(
        (aux::bit_floor::<Uint>(t) << 1) > t + blt, // nofmt
    );
    // ^^^ Correction factor
    let tau: Uint = blt - epsilon_tau; // Current meta-epoch

    let t_0: Uint = aux::shl::<Uint>(_1, tau) - tau;
    // ^^^ Opening epoch of meta-epoch
    let t_1: Uint = aux::shl::<Uint>(_1, tau + _1) - (tau + _1);
    // ^^^ Opening epoch of next meta-epoch
    let epsilon_b: Uint = aux::from_bool::<Uint>(t < h + t_0 && h + t_0 < t_1);
    // ^^^ uninvaded correction factor
    let B: Uint = std::cmp::max(
        aux::shr::<Uint>(S, tau + _1 - epsilon_b), // nofmt
        _1,                                        // nofmt
    );
    // ^^^ Num bunches available to h.v.

    let b_l: Uint = aux::modpow2::<Uint>(i, B); // Logical bunch index...
                                                // ... i.e., in order filled
                                                // (increasing nestedness/
                                                // decreasing init size r)

    // Need to calculate physical bunch index...
    // ... i.e., position among bunches left-to-right in buffer space
    let v: Uint = aux::bit_length::<Uint>(b_l);
    // ^^^ Nestedness depth level of physical bunch
    let w: Uint = aux::shr::<Uint>(S, v) * aux::from_bool::<Uint>(v > _0);
    // ^^^ Num bunches spaced between bunches in nest level
    let o: Uint = w >> 1; // Offset of nestedness level in physical bunch order
    let p: Uint = b_l - aux::bit_floor::<Uint>(b_l);
    // ^^^ Bunch position within nestedness level
    let b_p: Uint = o + w * p; // Physical bunch index...
                               // ... i.e., in left-to-right
                               // sequential bunch order

    // Need to calculate buffer position of b_p'th bunch
    let epsilon_k_b: Uint = aux::from_bool::<Uint>(b_l > _0);
    // ^^^ Correction factor for zeroth bunch...
    // ... i.e., bunch r=s at site k=0
    let k_b: Uint = (b_p << 1)
        + aux::popcount::<Uint>((S << 1) - b_p).wrapping_sub(
            &(_1 + epsilon_k_b), // nofmt
        );
    k_b + h // Calculate placement site, h.v. h is offset within bunch
}

/// Site selection implementation for tilted curation.
///
/// What buffer site should the T'th data item be stored to?
///
/// @template Uint Unsigned integer type for operands and return value.
/// @param S Buffer size.
///     Must be a power of two greater than 1, and 2 * S must not overflow Uint.
/// @param T Current logical time.
///     Must be less than 2^S - 1.
/// @returns The selected storage site, if any.
///     Returns None if no site should be selected (i.e., discard).
#[allow(non_snake_case)]
pub fn assign_storage_site<Uint: aux::UnsignedTrait>(
    S: Uint, // nofmt
    T: Uint, // nofmt
) -> Option<Uint> {
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
