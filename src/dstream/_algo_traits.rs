#[allow(non_snake_case)]
pub trait AssignStorageSiteTrait {
    fn _assign_storage_site<Uint: crate::_auxlib::UnsignedTrait>(S: Uint, T: Uint) -> Uint;
    fn assign_storage_site<Uint: crate::_auxlib::UnsignedTrait>(S: Uint, T: Uint) -> Option<Uint>;
}

#[allow(non_snake_case)]
pub trait HasIngestCapacityTrait {
    fn has_ingest_capacity<Uint: crate::_auxlib::UnsignedTrait>(S: Uint, T: Uint) -> bool;
}
