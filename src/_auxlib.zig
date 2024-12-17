const std = @import("std");
const testing = std.testing;

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
    return if (b < 64) a << @intCast(b) else 0;
}

test "bit_length" {
    try testing.expect(bit_length(0) == 0);
    try testing.expect(bit_length(1) == 1); // binary: 1 (highest bit = bit 0)
    try testing.expect(bit_length(2) == 2); // binary: 10 (highest bit = bit 1)
    try testing.expect(bit_length(3) == 2); // binary: 11 (highest bit = bit 1)
    try testing.expect(bit_length(4) == 3); // binary: 100 (highest bit = bit 2)
    try testing.expect(bit_length(0xFFFF_FFFF_FFFF_FFFF) == 64);
}

test "bit_floor" {
    try testing.expect(bit_floor(0) == 0);
    try testing.expect(bit_floor(1) == 1); // nearest power of 2 <= 1 is 1
    try testing.expect(bit_floor(2) == 2); // nearest power of 2 <= 2 is 2
    try testing.expect(bit_floor(3) == 2); // nearest power of 2 <= 3 is 2
    try testing.expect(bit_floor(4) == 4); // nearest power of 2 <= 4 is 4
    try testing.expect(bit_floor(5) == 4); // nearest power of 2 <= 5 is 4
    try testing.expect(bit_floor(0xFFFF_FFFF_FFFF_FFFF) == (1 << 63));
}

test "floor_subtract" {
    try testing.expect(floor_subtract(10, 5) == 5); // 10 - 5 = 5
    try testing.expect(floor_subtract(5, 10) == 0); // 5 - 10 = negative, so 0
    try testing.expect(floor_subtract(0, 0) == 0);
    try testing.expect(floor_subtract(100, 100) == 0);
    try testing.expect(floor_subtract(100, 101) == 0);
    try testing.expect(floor_subtract(100, 99) == 1); // 100 - 99 = 1
}

test "overflow_shl" {
    // overflow_shl shifts left by `b`, but caps the shift at 63 bits.
    try testing.expect(overflow_shl(1, 0) == 1); // 1 << 0 = 1
    try testing.expect(overflow_shl(1, 1) == 2); // 1 << 1 = 2
    try testing.expect(overflow_shl(1, 63) == (1 << 63));
    try testing.expect(overflow_shl(1, 64) == 0); // capped at 63
    try testing.expect(overflow_shl(2, 70) == 0); // also capped at 63
}
