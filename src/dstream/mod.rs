mod _algo_traits;
pub use _algo_traits::AssignStorageSiteTrait;
pub use _algo_traits::HasIngestCapacityTrait;

pub mod steady_algo;
pub use steady_algo::Algo as SteadyAlgo;
pub mod stretched_algo;
pub use stretched_algo::Algo as StretchedAlgo;
pub mod tilted_algo;
pub use tilted_algo::Algo as TiltedAlgo;
