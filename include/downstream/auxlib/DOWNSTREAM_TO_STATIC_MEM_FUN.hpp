#ifndef DOWNSTREAM_AUXLIB_TO_STATIC_MEM_FUN_HPP
#define DOWNSTREAM_AUXLIB_TO_STATIC_MEM_FUN_HPP

#include <type_traits>

// adapted from https://fekir.info/post/namespace-vs-struct/
#define DOWNSTREAM_TO_STATIC_MEM_FUN(ns, fun)                                  \
  static_assert(std::is_function<decltype(ns::fun)>::value, "not a function"); \
  constexpr static decltype(ns::fun)* fun = ns::fun

#endif  // DOWNSTREAM_AUXLIB_TO_STATIC_MEM_FUN_HPP
