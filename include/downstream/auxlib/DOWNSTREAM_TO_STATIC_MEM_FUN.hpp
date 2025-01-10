#pragma once
#ifndef DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP
#define DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP

#include <type_traits>

// adapted from https://fekir.info/post/namespace-vs-struct/
#define DOWNSTREAM_TO_STATIC_MEM_FUN(ns, fun, T)                              \
  static_assert(std::is_function<decltype(ns::fun<T>)>::value, "not a func"); \
  constexpr static decltype(ns::fun<T>)* fun = ns::fun<T>

#endif  // DOWNSTREAM_AUXLIB_DOWNSTREAM_TO_STATIC_MEM_FUN_HPP
