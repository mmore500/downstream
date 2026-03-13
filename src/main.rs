use downstream::_auxlib as aux;
use downstream::dstream;

#[allow(non_snake_case)]
fn dispatch_algo<Algo: dstream::AssignStorageSiteTrait + dstream::HasIngestCapacityTrait>(
    S: u64,
    T: u64,
    Smx: u64,
) {
    let has_capacity: bool = Algo::has_ingest_capacity::<u64>(S, T);
    debug_assert!(
        !aux::can_type_fit_value::<u8>(S)
            || !aux::can_type_fit_value::<u8>(T)
            || Algo::has_ingest_capacity::<u8>(
                S.try_into().unwrap(), // nofmt
                T.try_into().unwrap(), // nofmt
            ) == has_capacity
    );
    debug_assert!(
        !aux::can_type_fit_value::<u16>(S)
            || !aux::can_type_fit_value::<u16>(T)
            || Algo::has_ingest_capacity::<u16>(
                S.try_into().unwrap(), // nofmt
                T.try_into().unwrap(), // nofmt
            ) == has_capacity
    );
    debug_assert!(
        !aux::can_type_fit_value::<u32>(S)
            || !aux::can_type_fit_value::<u32>(T)
            || Algo::has_ingest_capacity::<u32>(
                S.try_into().unwrap(), // nofmt
                T.try_into().unwrap(), // nofmt
            ) == has_capacity
    );

    if has_capacity {
        let storage_site = Algo::assign_storage_site::<u64>(S, T);
        debug_assert!(
            !aux::can_type_fit_value::<u8>(S * Smx)
                || !aux::can_type_fit_value::<u8>(T)
                || Algo::assign_storage_site::<u8>(
                    S.try_into().unwrap(), // nofmt
                    T.try_into().unwrap(), // nofmt
                )
                .map(|x| (storage_site.is_some() // nofmt
                    && (x as u64 == storage_site.unwrap())))
                .unwrap_or(storage_site.is_none())
        );
        debug_assert!(
            !aux::can_type_fit_value::<u16>(S * Smx)
                || !aux::can_type_fit_value::<u16>(T)
                || Algo::assign_storage_site::<u16>(
                    S.try_into().unwrap(), // nofmt
                    T.try_into().unwrap(), // nofmt
                )
                .map(|x| (storage_site.is_some() // nofmt
                    && (x as u64 == storage_site.unwrap())))
                .unwrap_or(storage_site.is_none())
        );
        debug_assert!(
            !aux::can_type_fit_value::<u32>(S * Smx)
                || !aux::can_type_fit_value::<u32>(T)
                || Algo::assign_storage_site::<u32>(
                    S.try_into().unwrap(), // nofmt
                    T.try_into().unwrap(), // nofmt
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
        "dstream.circular_algo.assign_storage_site" => {
            dispatch_algo::<dstream::CircularAlgo>(S, T, 1) // nofmt
        }
        "dstream.compressing_algo.assign_storage_site" => {
            dispatch_algo::<dstream::CompressingAlgo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_circular_2_steady_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Circular2Steady3Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_circular_2_tilted_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Circular2Tilted3Algo>(S, T, 2) // nofmt
        }
        "dstream.hybrid_0_circular_3_steady_4_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Circular3Steady4Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_circular_5_steady_6_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Circular5Steady6Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_circular_7_steady_8_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Circular7Steady8Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_circular_11_steady_12_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Circular11Steady12Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_steady_1_circular_2_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Steady1Circular2Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Steady1Stretched2Algo>(S, T, 2) // nofmt
        }
        "dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Steady1Tilted2Algo>(S, T, 2) // nofmt
        }
        "dstream.hybrid_0_steady_1_tilted_2_circular_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Steady1Tilted2Circular3Algo>(S, T, 2)
            // nofmt
        }
        "dstream.hybrid_0_steady_2_circular_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Steady2Circular3Algo>(S, T, 1) // nofmt
        }
        "dstream.hybrid_0_steady_2_tilted_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Steady2Tilted3Algo>(S, T, 2) // nofmt
        }
        "dstream.hybrid_0_tilted_1_circular_2_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Tilted1Circular2Algo>(S, T, 2) // nofmt
        }
        "dstream.hybrid_0_tilted_2_circular_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Tilted2Circular3Algo>(S, T, 2) // nofmt
        }
        "dstream.hybrid_0_tilted_2_steady_3_algo.assign_storage_site" => {
            dispatch_algo::<dstream::Hybrid0Tilted2Steady3Algo>(S, T, 2) // nofmt
        }
        "dstream.steady_algo.assign_storage_site" => {
            dispatch_algo::<dstream::SteadyAlgo>(S, T, 1) // nofmt
        }
        "dstream.sticky_algo.assign_storage_site" => {
            dispatch_algo::<dstream::StickyAlgo>(S, T, 1) // nofmt
        }
        "dstream.stretched_algo.assign_storage_site" => {
            dispatch_algo::<dstream::StretchedAlgo>(S, T, 2) // nofmt
        }
        "dstream.tilted_algo.assign_storage_site" => {
            dispatch_algo::<dstream::TiltedAlgo>(S, T, 2) // nofmt
        }
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
