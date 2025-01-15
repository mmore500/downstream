use downstream::dstream;

fn main() {
    println!("Hello, world!");
    println!("{}", dstream::steady::assign_storage_site::<u32>(16, 2));
}
