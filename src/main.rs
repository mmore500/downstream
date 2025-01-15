use downstream::_auxlib as aux;
use downstream::dstream;

#[allow(non_snake_case)]
fn dispatch_algo<Algo: dstream::AssignStorageSiteTrait + dstream::HasIngestCapacityTrait>(
    S: u64,
    T: u64,
    Smx: u64,
) {
    let has_capacity = Algo::has_ingest_capacity::<u64>(S, T);
    debug_assert!(
        !aux::can_type_fit_value::<u8>(S)
            || !aux::can_type_fit_value::<u8>(T)
            || Algo::has_ingest_capacity::<u8>(
                S.try_into().unwrap(), //
                T.try_into().unwrap(), //
            ) == has_capacity
    );
    debug_assert!(
        !aux::can_type_fit_value::<u16>(S)
            || !aux::can_type_fit_value::<u16>(T)
            || Algo::has_ingest_capacity::<u16>(
                S.try_into().unwrap(), //
                T.try_into().unwrap(), //
            ) == has_capacity
    );
    debug_assert!(
        !aux::can_type_fit_value::<u32>(S)
            || !aux::can_type_fit_value::<u32>(T)
            || Algo::has_ingest_capacity::<u32>(
                //
                S.try_into().unwrap(), //
                T.try_into().unwrap(), //
            ) == has_capacity
    );

    if has_capacity {
        let storage_site = Algo::assign_storage_site::<u64>(S, T);
        debug_assert!(
            !aux::can_type_fit_value::<u8>(S * Smx)
                || !aux::can_type_fit_value::<u8>(T)
                || Algo::assign_storage_site::<u8>(
                    S.try_into().unwrap(), //
                    T.try_into().unwrap(), //
                )
                .map(|x| (storage_site.is_some() // nofmt
                    && (x as u64 == storage_site.unwrap())))
                .unwrap_or(storage_site.is_none())
        );
        debug_assert!(
            !aux::can_type_fit_value::<u16>(S * Smx)
                || !aux::can_type_fit_value::<u16>(T)
                || Algo::assign_storage_site::<u16>(
                    S.try_into().unwrap(), //
                    T.try_into().unwrap(), //
                )
                .map(|x| (storage_site.is_some() // nofmt
                    && (x as u64 == storage_site.unwrap())))
                .unwrap_or(storage_site.is_none())
        );
        debug_assert!(
            !aux::can_type_fit_value::<u32>(S * Smx)
                || !aux::can_type_fit_value::<u32>(T)
                || Algo::assign_storage_site::<u32>(
                    S.try_into().unwrap(), //
                    T.try_into().unwrap(), //
                )
                .map(|x| (storage_site.is_some() // nofmt
                    && (x as u64 == storage_site.unwrap())))
                .unwrap_or(storage_site.is_none())
        );

        if let Some(storage_site) = storage_site {
            println!("{}", storage_site);
        } else {
            println!("None");
        }
    } else {
        println!();
    }
}

#[allow(non_snake_case)]
fn dispatch(algo_name: &String, S: u64, T: u64) {
    match algo_name.as_str() {
        "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site" => todo!(),
        "dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site" => todo!(),
        "dstream.steady_algo.assign_storage_site" => dispatch_algo::<dstream::SteadyAlgo>(S, T, 1),
        "dstream.stretched_algo.assign_storage_site" => todo!(),
        "dstream.tilted_algo.assign_storage_site" => todo!(),
        _ => panic!("unknown algorithm/operation: {}", algo_name),
    }
}

#[allow(non_snake_case)]
pub fn main() {
    let args: Vec<String> = std::env::args().collect();
    let stdin = std::io::stdin();
    for line in stdin.lines() {
        let line = line.unwrap();
        let mut numbers = line.split_whitespace();
        let S: u64 = numbers.next().unwrap().parse().unwrap();
        let T: u64 = numbers.next().unwrap().parse().unwrap();
        dispatch(&args[1], S, T);
    }
}
