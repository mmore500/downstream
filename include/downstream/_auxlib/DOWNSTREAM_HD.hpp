#pragma once
#ifndef DOWNSTREAM_AUXLIB_DOWNSTREAM_HD_HPP
#define DOWNSTREAM_AUXLIB_DOWNSTREAM_HD_HPP

#ifndef DOWNSTREAM_HD
#ifdef __CUDACC__
#define DOWNSTREAM_HD __host__ __device__
#else
#define DOWNSTREAM_HD
#endif
#endif

#endif  // DOWNSTREAM_AUXLIB_DOWNSTREAM_HD_HPP
