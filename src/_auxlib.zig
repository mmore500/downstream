const std = @import("std");
const testing = std.testing;

pub fn assert_unsigned(comptime u: type) void {
    std.debug.assert(u == u8 or u == u16 or u == u32 or u == u64);
}

// Helper: Bit length (equivalent to std::bit_width in C++)
pub fn bit_length(comptime u: type, value: u) u {
    assert_unsigned(u);
    return @bitSizeOf(u) - @clz(value);
}

// Helper: Bit floor (equivalent to std::bit_floor in C++)
pub fn bit_floor(comptime u: type, value: u) u {
    assert_unsigned(u);
    if (0 < value) {
        return @as(u, 1) << @intCast(bit_length(u, value) - 1);
    } else {
        return 0;
    }
}

pub fn can_type_fit_value(comptime u: type, value: u64) bool {
    assert_unsigned(u);
    const ansatz: u = @truncate(value);
    const ansatz64: u64 = @intCast(ansatz);
    return ansatz64 == value;
}

pub fn floor_subtract(comptime u: type, minuend: u, subtrahend: u) u {
    assert_unsigned(u);
    return minuend - @min(minuend, subtrahend);
}

pub fn modpow2(comptime u: type, dividend: u, divisor: u) u {
    assert_unsigned(u);
    std.debug.assert(@popCount(divisor) == 1);
    return dividend & (divisor - 1);
}

pub fn overflow_shl(comptime u: type, a: u, b: u) u {
    assert_unsigned(u);
    return if (b < @bitSizeOf(u)) a << @intCast(b) else 0;
}

pub fn overflow_shr(comptime u: type, a: u, b: u) u {
    assert_unsigned(u);
    return if (b < @bitSizeOf(u)) a >> @intCast(b) else 0;
}

test "bit_length" {
    try testing.expect(bit_length(u32, 0) == 0);
    try testing.expect(bit_length(u32, 1) == 1); // binary: 1
    try testing.expect(bit_length(u32, 2) == 2); // binary: 10
    try testing.expect(bit_length(u32, 3) == 2); // binary: 11
    try testing.expect(bit_length(u32, 4) == 3); // binary: 100
    try testing.expect(bit_length(u64, 0xFFFF_FFFF_FFFF_FFFF) == 64);
}

test "bit_floor" {
    try testing.expect(bit_floor(u32, 0) == 0);
    try testing.expect(bit_floor(u32, 1) == 1); // power of 2 <= 1 is 1
    try testing.expect(bit_floor(u32, 2) == 2); // power of 2 <= 2 is 2
    try testing.expect(bit_floor(u32, 3) == 2); // power of 2 <= 3 is 2
    try testing.expect(bit_floor(u32, 4) == 4); // power of 2 <= 4 is 4
    try testing.expect(bit_floor(u32, 5) == 4); // power of 2 <= 5 is 4
    try testing.expect(bit_floor(u64, 0xFFFF_FFFF_FFFF_FFFF) == (1 << 63));
}

test "can_type_fit_value" {
    try testing.expect(can_type_fit_value(u8, 0));
    try testing.expect(can_type_fit_value(u8, 255));
    try testing.expect(!can_type_fit_value(u8, 256));
    try testing.expect(can_type_fit_value(u16, 0));
    try testing.expect(can_type_fit_value(u16, 65535));
    try testing.expect(!can_type_fit_value(u16, 65536));
    try testing.expect(can_type_fit_value(u32, 0));
    try testing.expect(can_type_fit_value(u32, 4294967295));
    try testing.expect(!can_type_fit_value(u32, 4294967296));
    try testing.expect(can_type_fit_value(u64, 0));
    try testing.expect(can_type_fit_value(u64, 18446744073709551615));
}

test "floor_subtract" {
    try testing.expect(floor_subtract(u32, 10, 5) == 5); // 10 - 5 = 5
    try testing.expect(floor_subtract(u32, 5, 10) == 0); // 5 - 10 = negative
    try testing.expect(floor_subtract(u32, 0, 0) == 0);
    try testing.expect(floor_subtract(u32, 100, 100) == 0);
    try testing.expect(floor_subtract(u32, 100, 101) == 0);
    try testing.expect(floor_subtract(u32, 100, 99) == 1); // 100 - 99 = 1
}

test "modpow2" {
    try testing.expect(modpow2(u32, 0, 1) == 0); // 0 % 1 = 0
    try testing.expect(modpow2(u32, 1, 1) == 0); // 1 % 1 = 0
    try testing.expect(modpow2(u32, 2, 1) == 0); // 2 % 1 = 0
    try testing.expect(modpow2(u32, 0, 2) == 0); // 0 % 2 = 0
    try testing.expect(modpow2(u32, 1, 2) == 1); // 1 % 2 = 1
    try testing.expect(modpow2(u32, 2, 2) == 0); // 2 % 2 = 0
    try testing.expect(modpow2(u32, 3, 2) == 1); // 3 % 2 = 1
    try testing.expect(modpow2(u64, 42, 0x8000_0000_0000_0000) == 42);
}

test "overflow_shl" {
    // overflow_shl shifts left by `b`, but caps the shift at 63 bits.
    try testing.expect(overflow_shl(u32, 1, 0) == 1); // 1 << 0 = 1
    try testing.expect(overflow_shl(u32, 1, 1) == 2); // 1 << 1 = 2
    try testing.expect(overflow_shl(u64, 1, 63) == (1 << 63));
    try testing.expect(overflow_shl(u32, 1, 64) == 0); // capped at 63
    try testing.expect(overflow_shl(u32, 2, 70) == 0); // also capped at 63
}

test "overflow_shr" {
    // overflow_shr shifts right by `b`, but caps the shift at 63 bits.
    try testing.expect(overflow_shr(u32, 2, 1) == 1); // 2 >> 1 = 1
    try testing.expect(overflow_shr(u32, 2, 2) == 0); // 2 >> 2 = 0
    try testing.expect(overflow_shr(u32, 2, 3) == 0); // 2 >> 2 = 0
    try testing.expect(overflow_shr(u64, 1 << 63, 63) == 1);
    try testing.expect(overflow_shr(u32, 1, 64) == 0); // capped at 63
    try testing.expect(overflow_shr(u32, 2, 70) == 0); // also capped at 63
}
