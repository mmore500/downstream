const std = @import("std");

const dstream = @import("downstream").dstream;

var bw = std.io.bufferedWriter(std.io.getStdOut().writer());
const stdout = bw.writer();

fn dispatch_algo(comptime algo: anytype, S: u32, T: u32) !void {
    const has_capacity = algo.has_ingest_capacity(u32, S, T);
    if (has_capacity) {
        const storage_site = algo.assign_storage_site(u32, S, T);
        if (storage_site == S) {
            try stdout.print("None\n", .{});
        } else {
            try stdout.print("{}\n", .{storage_site});
        }
    } else {
        try stdout.print("\n", .{});
    }
}

fn dispatch(algo_name: []const u8, values: []const u32) !void {
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

        var values = std.ArrayList(u32).init(std.heap.page_allocator);
        defer values.deinit();
        while (words.next()) |word| {
            const value = try std.fmt.parseInt(u32, word, 10);
            try values.append(value);
        }
        try dispatch(args[1], values.items);
    }
    try bw.flush(); // don't forget to flush!
}
