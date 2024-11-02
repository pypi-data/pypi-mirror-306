//===- ShardingInterfaceImpl.h - ------------------------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_DIALECT_TOSA_TRANSFORMS_SHARDINGINTERFACEIMPL_H_
#define MLIR_DIALECT_TOSA_TRANSFORMS_SHARDINGINTERFACEIMPL_H_

namespace mlir {

class DialectRegistry;

namespace tosa {

void registerShardingInterfaceExternalModels(DialectRegistry &registry);

} // namespace tosa
} // namespace mlir

#endif // MLIR_DIALECT_TOSA_TRANSFORMS_SHARDINGINTERFACEIMPL_H_
