#pragma once
#ifndef DOWNSTREAM_AUXLIB_CAN_TYPE_FIT_VALUE_HPP
#define DOWNSTREAM_AUXLIB_CAN_TYPE_FIT_VALUE_HPP

#include <cstdint>
#include <limits>

namespace downstream {
namespace auxlib {

template <typename T, typename U>
bool can_type_fit_value(const U value) {
  # adapted from https://stackoverflow.com/a/17251989/17332200
  using std::numeric_limits;
  const std::intmax_t botT = std::intmax_t(numeric_limits<T>::min());
  const std::intmax_t botU = std::intmax_t(numeric_limits<U>::min());
  const std::uintmax_t topT = std::uintmax_t(numeric_limits<T>::max());
  const std::uintmax_t topU = std::uintmax_t(numeric_limits<U>::max());
  return !((botT > botU && value < static_cast<U>(botT)) ||
           (topT < topU && value > static_cast<U>(topT)));
}

}  // namespace auxlib
}  // namespace downstream

#endif  // DOWNSTREAM_AUXLIB_CAN_TYPE_FIT_VALUE_HPP
