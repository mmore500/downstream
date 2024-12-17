const std = @import("std");

const auxlib = @import("../_auxlib.zig");

pub fn has_ingest_capacity(S: u64, T: u64) bool {
    _ = T;
    return (@popCount(S) == 1) and S > 1;
}

pub fn assign_storage_site(S: u64, T: u64) u64 {
    _ = S;
    _ = T;
    return 0;
}