/* Copyright 2019 The OpenXLA Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_SERVICE_GPU_RUNTIME_CHOLESKY_THUNK_H_
#define XLA_SERVICE_GPU_RUNTIME_CHOLESKY_THUNK_H_

#include <cstdint>

#include "absl/status/status.h"
#include "xla/service/buffer_assignment.h"
#include "xla/service/gpu/runtime/thunk.h"
#include "xla/stream_executor/blas.h"
#include "xla/stream_executor/device_memory.h"
#include "xla/stream_executor/gpu/gpu_asm_opts.h"
#include "xla/stream_executor/stream_executor.h"
#include "xla/xla_data.pb.h"

namespace xla {
namespace gpu {

// This class stores everything that StreamExecutor needs to launch a Cholesky
// decomposition (LAPACK potrf). It is generated by IrEmitter.
//
// As an implementation detail, we may run potrf (potentially in a loop, if
// batch_size >1), or potrfBatched.
//
// Thread-compatible.
class CholeskyThunk : public Thunk {
 public:
  CholeskyThunk(ThunkInfo thunk_info, const CholeskyOptions& options,
                se::GpuAsmOpts asm_opts, BufferAllocation::Slice a_buffer,
                BufferAllocation::Slice workspace_buffer,
                BufferAllocation::Slice info_buffer, PrimitiveType type,
                int64_t batch_size, int64_t n);

  CholeskyThunk(const CholeskyThunk&) = delete;
  CholeskyThunk& operator=(const CholeskyThunk&) = delete;

  absl::Status ExecuteOnStream(const ExecuteParams& params) override;

 private:
  se::GpuAsmOpts asm_opts_;
  se::blas::UpperLower uplo_;

  const BufferAllocation::Slice a_buffer_;
  const BufferAllocation::Slice workspace_buffer_;
  const BufferAllocation::Slice info_buffer_;

  const PrimitiveType type_;
  const int64_t batch_size_;
  const int64_t n_;
};

struct CholeskyParams {
  int64_t n;
  int64_t batch_size;
  se::blas::UpperLower uplo;
  se::DeviceMemoryBase a_buffer;
  se::DeviceMemoryBase workspace_buffer;
  se::DeviceMemoryBase info_buffer;
};
absl::Status RunCholesky(const se::GpuAsmOpts& asm_opts, PrimitiveType type,
                         CholeskyParams* params, se::Stream* stream);

}  // namespace gpu
}  // namespace xla

#endif  // XLA_SERVICE_GPU_RUNTIME_CHOLESKY_THUNK_H_
