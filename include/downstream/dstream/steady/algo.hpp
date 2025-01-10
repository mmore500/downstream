#pragma once
#ifndef DOWNSTREAM_DSTREAM_STEADY_ALGO_HPP
#define DOWNSTREAM_DSTREAM_STEADY_ALGO_HPP

#include "../../auxlib/DOWNSTREAM_TO_STATIC_MEM_FUN.hpp"
#include "./_assign_storage_site.hpp"
#include "./_has_ingest_capacity.hpp"

namespace downstream {
namespace dstream_steady {

namespace _ns = dstream_steady;

struct algo {
  algo() = delete;
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, _assign_storage_site);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, assign_storage_site);
  DOWNSTREAM_TO_STATIC_MEM_FUN(_ns, has_ingest_capacity);
};

}  // namespace dstream_steady
}  // namespace downstream

#endif  // DOWNSTREAM_DSTREAM_STEADY_ALGO_HPP
