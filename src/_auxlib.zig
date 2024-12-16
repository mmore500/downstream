// Helper: Bit floor (equivalent to std::bit_floor in C++)
pub fn bit_floor(value: u64) u64 {
    return 1 << (@bitSizeOf(value) - @clz(value) - 1);
}

// Helper: Bit length (equivalent to std::bit_width in C++)
pub fn bit_length(value: u64) u64 {
    return @bitSizeOf(value) - @clz(value);
}
