use std::mem::size_of;

// adapted from https://stackoverflow.com/a/26983395/17332200
pub trait UnsignedTrait:
    num_traits::PrimInt + num_traits::Unsigned + num_traits::FromPrimitive
{
}
impl<T> UnsignedTrait for T where
    T: num_traits::PrimInt + num_traits::Unsigned + num_traits::FromPrimitive
{
}

pub fn bit_size_of<T: UnsignedTrait>() -> T {
    unsafe { T::from_usize(size_of::<T>() * 8).unwrap_unchecked() }
}

pub fn bit_length<T: UnsignedTrait>(value: T) -> T {
    if value == T::zero() {
        T::zero()
    } else {
        let leading_: u32 = value.leading_zeros();
        let leading: T = unsafe { T::from_u32(leading_).unwrap_unchecked() };

        bit_size_of::<T>() - leading
    }
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
}
