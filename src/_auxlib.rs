// adapted from https://stackoverflow.com/a/26983395/17332200
pub trait UnsignedTrait:
    num_traits::PrimInt
    + num_traits::Unsigned
    + num_traits::FromPrimitive
    + num_traits::WrappingAdd
    + num_traits::WrappingMul
    + num_traits::WrappingSub
{
}
impl<T> UnsignedTrait for T where
    T: num_traits::PrimInt
        + num_traits::Unsigned
        + num_traits::FromPrimitive
        + num_traits::WrappingAdd
        + num_traits::WrappingMul
        + num_traits::WrappingSub
{
}

/// Number of bits in type `T`.
pub fn bit_size_of<T: UnsignedTrait>() -> T {
    unsafe { T::from_usize(std::mem::size_of::<T>() * 8).unwrap_unchecked() }
}

/// Returns the position of the highest set bit (1-based).
pub fn bit_length<T: UnsignedTrait>(value: T) -> T {
    if value == T::zero() {
        T::zero()
    } else {
        bit_size_of::<T>() - clz::<T>(value)
    }
}

/// Returns the largest power of 2 that is <= `value`.
/// If `value` is 0, returns 0.
pub fn bit_floor<T: UnsignedTrait>(value: T) -> T {
    if value > T::zero() {
        let length = bit_length(value);
        let shift = length - T::one();
        T::one() << unsafe { shift.to_usize().unwrap_unchecked() }
    } else {
        T::zero()
    }
}

/// Check if a `u64` value can fit into `T` without loss.
pub fn can_type_fit_value<T: UnsignedTrait>(value: u64) -> bool {
    T::from_u64(value).is_some()
}

/// Count leading zeros in binary representation, casting result to arg type.
pub fn clz<T: UnsignedTrait>(value: T) -> T {
    unsafe { T::from_u32(value.leading_zeros()).unwrap_unchecked() }
}

/// Count trailing zeros in binary representation, casting result to arg type.
pub fn ctz<T: UnsignedTrait>(value: T) -> T {
    unsafe { T::from_u32(value.trailing_zeros()).unwrap_unchecked() }
}

/// If `minuend >= subtrahend`, returns `minuend - subtrahend`.
/// Otherwise, returns 0.
pub fn floor_subtract<T: UnsignedTrait>(minuend: T, subtrahend: T) -> T {
    minuend - std::cmp::min(minuend, subtrahend)
}

/// Convert a boolean to a `T` value.
pub fn from_bool<T: UnsignedTrait>(value: bool) -> T {
    if value {
        T::one()
    } else {
        T::zero()
    }
}

/// Equivalent to `(dividend % divisor)` when `divisor` is a power-of-two.
pub fn modpow2<T: UnsignedTrait>(dividend: T, divisor: T) -> T {
    debug_assert_eq!(divisor.count_ones(), 1, "divisor must be a power of 2");
    dividend & (divisor - T::one())
}

/// Saturating shift-left,
pub fn overflow_shl<T: UnsignedTrait>(a: T, b: T) -> T {
    let size_bits = bit_size_of::<T>();
    if b >= size_bits {
        T::zero()
    } else {
        a << unsafe { b.to_usize().unwrap_unchecked() }
    }
}

/// Saturating shift-right,
pub fn overflow_shr<T: UnsignedTrait>(a: T, b: T) -> T {
    let size_bits = bit_size_of::<T>();
    if b >= size_bits {
        T::zero()
    } else {
        a >> unsafe { b.to_usize().unwrap_unchecked() }
    }
}

/// Count ones in binary representation, casting result to arg type.
pub fn popcount<T: UnsignedTrait>(value: T) -> T {
    unsafe { T::from_u32(value.count_ones()).unwrap_unchecked() }
}

/// Saturating shift-left,
pub fn shl<T: UnsignedTrait>(a: T, b: T) -> T {
    a << unsafe { b.to_usize().unwrap_unchecked() }
}

/// Saturating shift-right,
pub fn shr<T: UnsignedTrait>(a: T, b: T) -> T {
    a >> unsafe { b.to_usize().unwrap_unchecked() }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bit_size_of() {
        assert_eq!(bit_size_of::<u8>(), 8);
        assert_eq!(bit_size_of::<u16>(), 16);
        assert_eq!(bit_size_of::<u32>(), 32);
        assert_eq!(bit_size_of::<u64>(), 64);
    }

    #[test]
    fn test_bit_length() {
        assert_eq!(bit_length::<u32>(0), 0);
        assert_eq!(bit_length::<u32>(1), 1); // binary: 1
        assert_eq!(bit_length::<u32>(2), 2); // binary: 10
        assert_eq!(bit_length::<u32>(3), 2); // binary: 11
        assert_eq!(bit_length::<u32>(4), 3); // binary: 100
        assert_eq!(bit_length::<u64>(0xFFFF_FFFF_FFFF_FFFF), 64);
    }

    #[test]
    fn test_bit_floor() {
        assert_eq!(bit_floor::<u32>(0), 0);
        assert_eq!(bit_floor::<u32>(1), 1); // power of 2 <= 1 is 1
        assert_eq!(bit_floor::<u32>(2), 2); // power of 2 <= 2 is 2
        assert_eq!(bit_floor::<u32>(3), 2); // power of 2 <= 3 is 2
        assert_eq!(bit_floor::<u32>(4), 4); // power of 2 <= 4 is 4
        assert_eq!(bit_floor::<u32>(5), 4); // power of 2 <= 5 is 4
        assert_eq!(bit_floor::<u64>(0xFFFF_FFFF_FFFF_FFFF), 1 << 63);
    }

    #[test]
    fn test_clz() {
        assert_eq!(clz::<u32>(0), 32);
        assert_eq!(clz::<u32>(1), 31);
        assert_eq!(clz::<u32>(2), 30);
        assert_eq!(clz::<u32>(3), 30);
        assert_eq!(clz::<u32>(4), 29);
        assert_eq!(clz::<u64>(0xFFFF_FFFF_FFFF_FFFF), 0);
    }

    #[test]
    fn test_ctz() {
        assert_eq!(ctz::<u32>(0), 32);
        assert_eq!(ctz::<u32>(1), 0);
        assert_eq!(ctz::<u32>(2), 1);
        assert_eq!(ctz::<u32>(3), 0);
        assert_eq!(ctz::<u32>(4), 2);
        assert_eq!(ctz::<u64>(0xFFFF_FFFF_FFFF_FFFF), 0);
    }

    #[test]
    fn test_can_type_fit_value() {
        assert!(can_type_fit_value::<u8>(0));
        assert!(can_type_fit_value::<u8>(255));
        assert!(!can_type_fit_value::<u8>(256));

        assert!(can_type_fit_value::<u16>(0));
        assert!(can_type_fit_value::<u16>(65535));
        assert!(!can_type_fit_value::<u16>(65536));

        assert!(can_type_fit_value::<u32>(0));
        assert!(can_type_fit_value::<u32>(4294967295));
        assert!(!can_type_fit_value::<u32>(4294967296));

        assert!(can_type_fit_value::<u64>(0));
        assert!(can_type_fit_value::<u64>(18446744073709551615));
    }

    #[test]
    fn test_floor_subtract() {
        assert_eq!(floor_subtract::<u32>(10, 5), 5); // 10 - 5 = 5
        assert_eq!(floor_subtract::<u32>(5, 10), 0); // 5 - 10 = 0
        assert_eq!(floor_subtract::<u32>(0, 0), 0);
        assert_eq!(floor_subtract::<u32>(100, 100), 0);
        assert_eq!(floor_subtract::<u32>(100, 101), 0);
        assert_eq!(floor_subtract::<u32>(100, 99), 1); // 100 - 99 = 1
    }

    #[test]
    fn test_from_bool() {
        assert_eq!(from_bool::<u32>(false), 0);
        assert_eq!(from_bool::<u32>(true), 1);
        assert_eq!(from_bool::<u16>(true), 1);
    }

    #[test]
    fn test_modpow2() {
        assert_eq!(modpow2::<u32>(0, 1), 0);
        assert_eq!(modpow2::<u32>(1, 1), 0);
        assert_eq!(modpow2::<u32>(2, 1), 0);
        assert_eq!(modpow2::<u32>(0, 2), 0);
        assert_eq!(modpow2::<u32>(1, 2), 1);
        assert_eq!(modpow2::<u32>(2, 2), 0);
        assert_eq!(modpow2::<u32>(3, 2), 1);
        assert_eq!(modpow2::<u64>(42, 0x8000_0000_0000_0000), 42);
    }

    #[test]
    fn test_overflow_shl() {
        assert_eq!(overflow_shl::<u32>(1, 0), 1);
        assert_eq!(overflow_shl::<u32>(1, 1), 2);
        assert_eq!(overflow_shl::<u64>(1, 63), 1 << 63);
        assert_eq!(overflow_shl::<u32>(1, 64), 0);
        assert_eq!(overflow_shl::<u32>(2, 70), 0);
    }

    #[test]
    fn test_overflow_shr() {
        assert_eq!(overflow_shr::<u32>(2, 1), 1);
        assert_eq!(overflow_shr::<u32>(2, 2), 0);
        assert_eq!(overflow_shr::<u32>(2, 3), 0);
        assert_eq!(overflow_shr::<u64>(1 << 63, 63), 1);
        assert_eq!(overflow_shr::<u32>(1, 64), 0);
        assert_eq!(overflow_shr::<u32>(2, 70), 0);
    }

    #[test]
    fn test_popcount() {
        assert_eq!(popcount::<u32>(0), 0);
        assert_eq!(popcount::<u32>(1), 1);
        assert_eq!(popcount::<u32>(2), 1);
        assert_eq!(popcount::<u32>(3), 2);
        assert_eq!(popcount::<u32>(4), 1);
        assert_eq!(popcount::<u32>(5), 2);
        assert_eq!(popcount::<u32>(6), 2);
    }

    #[test]
    fn test_shl() {
        assert_eq!(shl::<u32>(1, 0), 1);
        assert_eq!(shl::<u32>(1, 1), 2);
        assert_eq!(shl::<u64>(1, 63), 1 << 63);
    }

    #[test]
    fn test_shr() {
        assert_eq!(shr::<u32>(2, 1), 1);
        assert_eq!(shr::<u32>(2, 2), 0);
        assert_eq!(shr::<u32>(2, 3), 0);
        assert_eq!(shr::<u64>(1 << 63, 63), 1);
    }
}
