// Helper: Bit length (equivalent to std::bit_width in C++)
pub fn bit_length(value: u64) u64 {
    return @bitSizeOf(u64) - @clz(value);
}

// Helper: Bit floor (equivalent to std::bit_floor in C++)
pub fn bit_floor(value: u64) u64 {
    return @as(u64, 1) << @intCast(value - 1);
}
