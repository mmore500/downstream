mod _auxlib;

pub fn add(left: u64, right: u64) -> u64 {
    left + right + _auxlib::mul(0, right)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
