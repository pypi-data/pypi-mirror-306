/*
 *  Copyright 2008-2018 NVIDIA Corporation
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

#include <thrust/detail/type_traits.h>

#if _CCCL_STD_VER >= 2011
  #include <thrust/detail/execute_with_dependencies.h>
#endif

THRUST_NAMESPACE_BEGIN

namespace detail
{

template <typename Allocator, template <typename> class BaseSystem>
struct execute_with_allocator
  : BaseSystem<execute_with_allocator<Allocator, BaseSystem> >
{
private:
  typedef BaseSystem<execute_with_allocator<Allocator, BaseSystem> > super_t;

  Allocator alloc;

public:
  _CCCL_HOST_DEVICE
  execute_with_allocator(super_t const& super, Allocator alloc_)
    : super_t(super), alloc(alloc_)
  {}

  _CCCL_EXEC_CHECK_DISABLE
  _CCCL_HOST_DEVICE
  execute_with_allocator(Allocator alloc_)
    : alloc(alloc_)
  {}

  typename remove_reference<Allocator>::type& get_allocator() { return alloc; }

#if _CCCL_STD_VER >= 2011
  template<typename ...Dependencies>
  _CCCL_HOST
  execute_with_allocator_and_dependencies<Allocator, BaseSystem, Dependencies...>
  after(Dependencies&& ...dependencies) const
  {
    return { alloc, capture_as_dependency(THRUST_FWD(dependencies))... };
  }

  template<typename ...Dependencies>
  _CCCL_HOST
  execute_with_allocator_and_dependencies<Allocator, BaseSystem, Dependencies...>
  after(std::tuple<Dependencies...>& dependencies) const
  {
      return { alloc, capture_as_dependency(dependencies) };
  }
  template<typename ...Dependencies>
  _CCCL_HOST
  execute_with_allocator_and_dependencies<Allocator, BaseSystem, Dependencies...>
  after(std::tuple<Dependencies...>&& dependencies) const
  {
      return { alloc, capture_as_dependency(std::move(dependencies)) };
  }

  template<typename ...Dependencies>
  _CCCL_HOST
  execute_with_allocator_and_dependencies<Allocator, BaseSystem, Dependencies...>
  rebind_after(Dependencies&& ...dependencies) const
  {
    return { alloc, capture_as_dependency(THRUST_FWD(dependencies))... };
  }

  template<typename ...Dependencies>
  _CCCL_HOST
  execute_with_allocator_and_dependencies<Allocator, BaseSystem, Dependencies...>
  rebind_after(std::tuple<Dependencies...>& dependencies) const
  {
      return { alloc, capture_as_dependency(dependencies) };
  }
  template<typename ...Dependencies>
  _CCCL_HOST
  execute_with_allocator_and_dependencies<Allocator, BaseSystem, Dependencies...>
  rebind_after(std::tuple<Dependencies...>&& dependencies) const
  {
      return { alloc, capture_as_dependency(std::move(dependencies)) };
  }
#endif
};

} // namespace detail

THRUST_NAMESPACE_END
