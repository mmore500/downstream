#pragma once
#ifndef DOWNSTREAM_DSTREAM_STRETCHED_ALGO_HPP
#define DOWNSTREAM_DSTREAM_STRETCHED_ALGO_HPP

#include <concepts>

#include "../../auxlib/DOWNSTREAM_TO_STATIC_MEM_FUN.hpp"
#include "../../auxlib/DOWNSTREAM_UINT.hpp"
#include "./_assign_storage_site.hpp"
#include "./_get_algo_name.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_stretched {

namespace _ns = dstream_stretched;

/**
 * Template-friendly packaging of stretched curation algorithm components.
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

}  // namespace dstream_stretched
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STRETCHED_ALGO_HPP
