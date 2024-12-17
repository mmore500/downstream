const std = @import("std");
const testing = std.testing;

// Helper: Bit length (equivalent to std::bit_width in C++)
pub fn bit_length(value: u32) u32 {
    return @bitSizeOf(u32) - @clz(value);
}

// Helper: Bit floor (equivalent to std::bit_floor in C++)
pub fn bit_floor(value: u32) u32 {
    if (0 < value) {
        return @as(u32, 1) << @intCast(bit_length(value) - 1);
    } else {
        return 0;
    }
}

pub fn floor_subtract(minuend: u32, subtrahend: u32) u32 {
    return minuend - @min(minuend, subtrahend);
}

pub fn modpow2(dividend: u32, divisor: u32) u32 {
    std.debug.assert(@popCount(divisor) == 1);
    return dividend & (divisor - 1);
}

pub fn overflow_shl(a: u32, b: u32) u32 {
    return if (b < @bitSizeOf(u32)) a << @intCast(b) else 0;
}

test "bit_length" {
    try testing.expect(bit_length(0) == 0);
    try testing.expect(bit_length(1) == 1); // binary: 1
    try testing.expect(bit_length(2) == 2); // binary: 10
    try testing.expect(bit_length(3) == 2); // binary: 11
    try testing.expect(bit_length(4) == 3); // binary: 100
}

test "bit_floor" {
    try testing.expect(bit_floor(0) == 0);
    try testing.expect(bit_floor(1) == 1); // power of 2 <= 1 is 1
    try testing.expect(bit_floor(2) == 2); // power of 2 <= 2 is 2
    try testing.expect(bit_floor(3) == 2); // power of 2 <= 3 is 2
    try testing.expect(bit_floor(4) == 4); // power of 2 <= 4 is 4
    try testing.expect(bit_floor(5) == 4); // power of 2 <= 5 is 4
}

test "floor_subtract" {
    try testing.expect(floor_subtract(10, 5) == 5); // 10 - 5 = 5
    try testing.expect(floor_subtract(5, 10) == 0); // 5 - 10 = negative
    try testing.expect(floor_subtract(0, 0) == 0);
    try testing.expect(floor_subtract(100, 100) == 0);
    try testing.expect(floor_subtract(100, 101) == 0);
    try testing.expect(floor_subtract(100, 99) == 1); // 100 - 99 = 1
}

test "modpow2" {
    try testing.expect(modpow2(0, 1) == 0); // 0 % 1 = 0
    try testing.expect(modpow2(1, 1) == 0); // 1 % 1 = 0
    try testing.expect(modpow2(2, 1) == 0); // 2 % 1 = 0
    try testing.expect(modpow2(0, 2) == 0); // 0 % 2 = 0
    try testing.expect(modpow2(1, 2) == 1); // 1 % 2 = 1
    try testing.expect(modpow2(2, 2) == 0); // 2 % 2 = 0
    try testing.expect(modpow2(3, 2) == 1); // 3 % 2 = 1
}

test "overflow_shl" {
    // overflow_shl shifts left by `b`, but caps the shift at 63 bits.
    try testing.expect(overflow_shl(1, 0) == 1); // 1 << 0 = 1
    try testing.expect(overflow_shl(1, 1) == 2); // 1 << 1 = 2
    try testing.expect(overflow_shl(1, 64) == 0); // capped at 63
    try testing.expect(overflow_shl(2, 70) == 0); // also capped at 63
}
