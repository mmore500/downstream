mod _auxlib;

pub fn add(left: u64, right: u64) -> u64 {
    _auxlib::bit_length(left);
    left + right
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
