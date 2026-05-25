#pragma once
#ifndef DOWNSTREAM_AUXLIB_DOWNSTREAM_CUDA_HD_HPP
#define DOWNSTREAM_AUXLIB_DOWNSTREAM_CUDA_HD_HPP

// Function-attribute prefix that expands to `__host__ __device__` under nvcc
// and to nothing otherwise. Define `DOWNSTREAM_CUDA_HD` before including this
// header (or via the build system) to override.
#ifndef DOWNSTREAM_CUDA_HD
#ifdef __CUDACC__
#define DOWNSTREAM_CUDA_HD __host__ __device__
#else
#define DOWNSTREAM_CUDA_HD
#endif
#endif

#endif  // DOWNSTREAM_AUXLIB_DOWNSTREAM_CUDA_HD_HPP
