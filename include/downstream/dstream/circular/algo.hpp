#pragma once
#ifndef DOWNSTREAM_DSTREAM_CIRCULAR_ALGO_HPP
#define DOWNSTREAM_DSTREAM_CIRCULAR_ALGO_HPP

#include <concepts>

#include "../../_auxlib/DOWNSTREAM_TO_STATIC_MEM_FUN.hpp"
#include "../../_auxlib/DOWNSTREAM_UINT.hpp"
#include "./_assign_storage_site.hpp"
#include "./_get_algo_name.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_circular {

namespace _ns = dstream_circular;

/**
 * Template-friendly packaging of circular curation algorithm components.
 *
 * @tparam UINT Unsigned integer type for operands and return value.
 */
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
struct algo {
  algo() = delete;
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, _assign_storage_site, UINT);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, assign_storage_site, UINT);
  DOWNSTREAM_TO_STATIC_MEM_FUN_(_ns, get_algo_name);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, has_ingest_capacity, UINT);
};

}  // namespace dstream_circular
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_CIRCULAR_ALGO_HPP
