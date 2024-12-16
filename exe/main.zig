const std = @import("std");

const dstream = @import("downstream").dstream;

fn dispatch(algo_name: []const u8, values: []const u64) u64 {
    if (std.mem.eql(u8, algo_name, "steady_algo.assign_storage_site")) {
        return dstream.steady_algo.assign_storage_site(values[0], values[1]);
    } else if (std.mem.eql(
        u8,
        algo_name,
        "stretched_algo.assign_storage_site",
    )) {
        return dstream.stretched_algo.assign_storage_site(values[0], values[1]);
    } else if (std.mem.eql(u8, algo_name, "tilted_algo.assign_storage_site")) {
        return dstream.tilted_algo.assign_storage_site(values[0], values[1]);
    } else {
        std.debug.panic("unknown algorithm/operation: {s}\n", .{algo_name});
    }
}

pub fn main() !void {
    const args = try std.process.argsAlloc(std.heap.page_allocator);
    defer std.process.argsFree(std.heap.page_allocator, args);

    var reader = std.io.getStdIn().reader();
    const alloc = std.heap.page_allocator;

    const stdout_file = std.io.getStdOut().writer();
    var bw = std.io.bufferedWriter(stdout_file);
    const stdout = bw.writer();

    while (try reader.readUntilDelimiterOrEofAlloc(alloc, '\n', 4096)) |line| {
        var words = std.mem.split(u8, line, " ");

        var values = std.ArrayList(u64).init(std.heap.page_allocator);
        defer values.deinit();
        while (words.next()) |word| {
            const value = try std.fmt.parseInt(u64, word, 10);
            try values.append(value);
        }

        try stdout.print("{}\n", .{dispatch(args[1], values.items)});
    }
    try bw.flush(); // don't forget to flush!
}
