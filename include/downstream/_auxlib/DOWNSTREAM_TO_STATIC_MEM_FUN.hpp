#pragma once
#ifndef DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP
#define DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP

#include <type_traits>

#include "./DOWNSTREAM_CUDA_HD.hpp"

// adapted from https://fekir.info/post/namespace-vs-struct/
#define DOWNSTREAM_TO_STATIC_MEM_FUN(ns, fun, T)                              \
  static_assert(                                                              \
      std::is_function_v<std::remove_reference_t<decltype(ns::fun<T>)>>,      \
      "not a func");                                                          \
  DOWNSTREAM_CUDA_HD                                                          \
  static auto fun(T arg1, T arg2) -> decltype(ns::fun<T>(arg1, arg2)) {       \
    return ns::fun<T>(arg1, arg2);                                            \
  }

#define DOWNSTREAM_TO_STATIC_MEM_FUN_(ns, fun)                          \
  static_assert(                                                        \
      std::is_function_v<std::remove_reference_t<decltype(ns::fun)>>,   \
      "not a func");                                                    \
  DOWNSTREAM_CUDA_HD                                                    \
  static auto fun() -> decltype(ns::fun()) { return ns::fun(); }

#endif  // DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP
