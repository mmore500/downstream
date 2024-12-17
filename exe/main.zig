const std = @import("std");

const dstream = @import("downstream").dstream;

var bw = std.io.bufferedWriter(std.io.getStdOut().writer());
const stdout = bw.writer();

fn dispatch_steady_algo_assign_storage_site(S: u32, T: u32) !void {
    if (dstream.steady_algo.has_ingest_capacity(u32, S, T)) {
        const result = dstream.steady_algo.assign_storage_site(u32, S, T);
        if (result == S) {
            try stdout.print("None\n", .{});
        } else {
            try stdout.print("{}\n", .{result});
        }
    } else {
        try stdout.print("\n", .{});
    }
}

fn dispatch_stretched_algo_assign_storage_site(S: u32, T: u32) !void {
    if (dstream.stretched_algo.has_ingest_capacity(u32, S, T)) {
        const result = dstream.stretched_algo.assign_storage_site(u32, S, T);
        if (result == S) {
            try stdout.print("None\n", .{});
        } else {
            try stdout.print("{}\n", .{result});
        }
    } else {
        try stdout.print("\n", .{});
    }
}

fn dispatch_tilted_algo_assign_storage_site(S: u32, T: u32) !void {
    if (dstream.tilted_algo.has_ingest_capacity(u32, S, T)) {
        const result = dstream.tilted_algo.assign_storage_site(u32, S, T);
        if (result == S) {
            try stdout.print("None\n", .{});
        } else {
            try stdout.print("{}\n", .{result});
        }
    } else {
        try stdout.print("\n", .{});
    }
}

fn dispatch(algo_name: []const u8, values: []const u32) !void {
    const steady_assign = "steady_algo.assign_storage_site";
    const stretched_assign = "stretched_algo.assign_storage_site";
    const tilted_assign = "tilted_algo.assign_storage_site";

    if (std.mem.eql(u8, algo_name, steady_assign)) {
        try dispatch_steady_algo_assign_storage_site(values[0], values[1]);
    } else if (std.mem.eql(u8, algo_name, stretched_assign)) {
        try dispatch_stretched_algo_assign_storage_site(values[0], values[1]);
    } else if (std.mem.eql(u8, algo_name, tilted_assign)) {
        try dispatch_tilted_algo_assign_storage_site(values[0], values[1]);
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
