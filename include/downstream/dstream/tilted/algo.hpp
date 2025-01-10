#pragma once
#ifndef DOWNSTREAM_DSTREAM_TILTED_ALGO_HPP
#define DOWNSTREAM_DSTREAM_TILTED_ALGO_HPP

#include <concepts>

#include "../../auxlib/DOWNSTREAM_TO_STATIC_MEM_FUN.hpp"
#include "../../auxlib/DOWNSTREAM_UINT.hpp"
#include "./_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_tilted {

namespace _ns = dstream_tilted;

template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
struct algo {
  algo() = delete;
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, _assign_storage_site, UINT);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, assign_storage_site, UINT);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, has_ingest_capacity, UINT);
};

}  // namespace dstream_tilted
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_TILTED_ALGO_HPP
