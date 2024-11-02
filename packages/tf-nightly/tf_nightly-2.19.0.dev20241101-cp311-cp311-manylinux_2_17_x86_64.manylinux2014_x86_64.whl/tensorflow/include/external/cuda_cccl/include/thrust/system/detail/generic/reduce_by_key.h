/*
 *  Copyright 2008-2013 NVIDIA Corporation
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */


#pragma once

#include <thrust/detail/config.h>

#if defined(_CCCL_IMPLICIT_SYSTEM_HEADER_GCC)
#  pragma GCC system_header
#elif defined(_CCCL_IMPLICIT_SYSTEM_HEADER_CLANG)
#  pragma clang system_header
#elif defined(_CCCL_IMPLICIT_SYSTEM_HEADER_MSVC)
#  pragma system_header
#endif // no system header
#include <thrust/system/detail/generic/tag.h>
#include <thrust/iterator/iterator_traits.h>

THRUST_NAMESPACE_BEGIN
namespace system
{
namespace detail
{
namespace generic
{


template<typename DerivedPolicy,
         typename InputIterator1,
         typename InputIterator2,
         typename OutputIterator1,
         typename OutputIterator2>
_CCCL_HOST_DEVICE
  thrust::pair<OutputIterator1,OutputIterator2>
    reduce_by_key(thrust::execution_policy<DerivedPolicy> &exec,
                  InputIterator1 keys_first,
                  InputIterator1 keys_last,
                  InputIterator2 values_first,
                  OutputIterator1 keys_output,
                  OutputIterator2 values_output);

template<typename DerivedPolicy,
         typename InputIterator1,
         typename InputIterator2,
         typename OutputIterator1,
         typename OutputIterator2,
         typename BinaryPredicate>
_CCCL_HOST_DEVICE
  thrust::pair<OutputIterator1,OutputIterator2>
    reduce_by_key(thrust::execution_policy<DerivedPolicy> &exec,
                  InputIterator1 keys_first,
                  InputIterator1 keys_last,
                  InputIterator2 values_first,
                  OutputIterator1 keys_output,
                  OutputIterator2 values_output,
                  BinaryPredicate binary_pred);

template<typename DerivedPolicy,
         typename InputIterator1,
         typename InputIterator2,
         typename OutputIterator1,
         typename OutputIterator2,
         typename BinaryPredicate,
         typename BinaryFunction>
_CCCL_HOST_DEVICE
  thrust::pair<OutputIterator1,OutputIterator2>
    reduce_by_key(thrust::execution_policy<DerivedPolicy> &exec,
                  InputIterator1 keys_first,
                  InputIterator1 keys_last,
                  InputIterator2 values_first,
                  OutputIterator1 keys_output,
                  OutputIterator2 values_output,
                  BinaryPredicate binary_pred,
                  BinaryFunction binary_op);


} // end namespace generic
} // end namespace detail
} // end namespace system
THRUST_NAMESPACE_END

#include <thrust/system/detail/generic/reduce_by_key.inl>

