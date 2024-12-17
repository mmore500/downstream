// Helper: Bit length (equivalent to std::bit_width in C++)
pub fn bit_length(value: u64) u64 {
    return @bitSizeOf(u64) - @clz(value);
}

// Helper: Bit floor (equivalent to std::bit_floor in C++)
pub fn bit_floor(value: u64) u64 {
    if (0 < value) {
        return @as(u64, 1) << @intCast(bit_length(value) - 1);
    } else {
        return 0;
    }
}

pub fn floor_subtract(minuend: u64, subtrahend: u64) u64 {
    return minuend - @min(minuend, subtrahend);
}

pub fn overflow_shl(a: u64, b: u64) u64 {
    const b6: u6 = @intCast(@min(b, 63));
    return @shlWithOverflow(a, b6)[0];
}
