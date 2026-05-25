#pragma once
#ifndef DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP
#define DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP

#include <type_traits>

// adapted from https://fekir.info/post/namespace-vs-struct/
//
// `decltype` on an unparenthesized id-expression naming a function yields the
// function type under g++ but a reference to function under nvcc; normalize
// via `std::remove_reference_t` so both produce a function-pointer member.
#define DOWNSTREAM_TO_STATIC_MEM_FUN(ns, fun, T)                         \
  static_assert(                                                         \
      std::is_function_v<std::remove_reference_t<decltype(ns::fun<T>)>>, \
      "not a func");                                                     \
  constexpr static std::remove_reference_t<decltype(ns::fun<T>)>* fun =  \
      ns::fun<T>

#define DOWNSTREAM_TO_STATIC_MEM_FUN_(ns, fun)                        \
  static_assert(                                                      \
      std::is_function_v<std::remove_reference_t<decltype(ns::fun)>>, \
      "not a func");                                                  \
  constexpr static std::remove_reference_t<decltype(ns::fun)>* fun = ns::fun

#endif  // DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP
