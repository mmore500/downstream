const std = @import("std");

const dstream = @import("downstream").dstream;
const aux = @import("downstream")._auxlib;

var bw = std.io.bufferedWriter(std.io.getStdOut().writer());
const stdout = bw.writer();

fn dispatch_algo(comptime algo: anytype, S: u64, T: u64) !void {
    const has_capacity = algo.has_ingest_capacity(u64, S, T);

    std.debug.assert( //
        !aux.can_type_fit_value(u8, S) or //
        !aux.can_type_fit_value(u8, T + 1) or //
        (algo.has_ingest_capacity(u8, @intCast(S), @intCast(T)) //
        == //
        has_capacity) //
    );
    std.debug.assert( //
        !aux.can_type_fit_value(u16, S) or //
        !aux.can_type_fit_value(u16, T + 1) or //
        (algo.has_ingest_capacity(u16, @intCast(S), @intCast(T)) //
        == //
        has_capacity) //
    );
    std.debug.assert( //
        !aux.can_type_fit_value(u32, S) or //
        !aux.can_type_fit_value(u32, T + 1) or //
        (algo.has_ingest_capacity(u32, @intCast(S), @intCast(T)) //
        == //
        has_capacity) //
    );

    if (has_capacity) {
        const storage_site = algo.assign_storage_site(u64, S, T);
        std.debug.assert( //
            !aux.can_type_fit_value(u8, 2 * S) or //
            !aux.can_type_fit_value(u8, 2 * (T + 1)) or //
            (algo.assign_storage_site(u8, @intCast(S), @intCast(T)) //
            == //
            storage_site) //
        );
        std.debug.assert( //
            !aux.can_type_fit_value(u16, 2 * S) or //
            !aux.can_type_fit_value(u16, 2 * (T + 1)) or //
            (algo.assign_storage_site(u16, @intCast(S), @intCast(T)) //
            == //
            storage_site) //
        );
        std.debug.assert( //
            !aux.can_type_fit_value(u32, 2 * S) or //
            !aux.can_type_fit_value(u32, 2 * (T + 1)) or //
            (algo.assign_storage_site(u32, @intCast(S), @intCast(T)) //
            == //
            storage_site) //
        );

        if (storage_site == S) {
            try stdout.print("None\n", .{});
        } else {
            try stdout.print("{}\n", .{storage_site});
        }
    } else {
        try stdout.print("\n", .{});
    }
}

fn dispatch(algo_name: []const u8, values: []const u64) !void {
    const hybrid_0_steady_1_stretched_2_assign = "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site";
    const hybrid_0_steady_1_tilted_2_assign = "dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site";
    const steady_assign = "dstream.steady_algo.assign_storage_site";
    const stretched_assign = "dstream.stretched_algo.assign_storage_site";
    const tilted_assign = "dstream.tilted_algo.assign_storage_site";

    if (std.mem.eql(u8, algo_name, hybrid_0_steady_1_stretched_2_assign)) {
        try dispatch_algo(
            dstream.hybrid_0_steady_1_stretched_2_algo,
            values[0],
            values[1],
        );
    } else if (std.mem.eql(u8, algo_name, hybrid_0_steady_1_tilted_2_assign)) {
        try dispatch_algo(
            dstream.hybrid_0_steady_1_tilted_2_algo,
            values[0],
            values[1],
        );
    } else if (std.mem.eql(u8, algo_name, steady_assign)) {
        try dispatch_algo(
            dstream.steady_algo,
            values[0],
            values[1],
        );
    } else if (std.mem.eql(u8, algo_name, stretched_assign)) {
        try dispatch_algo(
            dstream.stretched_algo,
            values[0],
            values[1],
        );
    } else if (std.mem.eql(u8, algo_name, tilted_assign)) {
        try dispatch_algo(
            dstream.tilted_algo,
            values[0],
            values[1],
        );
    } else {
        std.debug.panic("unknown algorithm/operation: {s}\n", .{algo_name});
    }
}

pub fn main() !void {
    const args = try std.process.argsAlloc(std.heap.page_allocator);
    defer std.process.argsFree(std.heap.page_allocator, args);

    var reader = std.io.getStdIn().reader();
    const alloc = std.heap.page_allocator;
    while (try reader.readUntilDelimiterOrEofAlloc(alloc, '\n', 4096)) |line| {
        var words = std.mem.split(u8, line, " ");

        var values = std.ArrayList(u64).init(std.heap.page_allocator);
        defer values.deinit();
        while (words.next()) |word| {
            const value = try std.fmt.parseInt(u64, word, 10);
            try values.append(value);
        }
        try dispatch(args[1], values.items);
    }
    try bw.flush(); // don't forget to flush!
}
