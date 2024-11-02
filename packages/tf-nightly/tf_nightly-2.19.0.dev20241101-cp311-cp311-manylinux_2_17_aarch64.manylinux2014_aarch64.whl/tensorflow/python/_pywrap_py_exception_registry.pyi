# Copyright 2023 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from typing import ClassVar

TF_ABORTED: TF_Code
TF_CANCELLED: TF_Code
TF_DATA_LOSS: TF_Code
TF_DEADLINE_EXCEEDED: TF_Code
TF_FAILED_PRECONDITION: TF_Code
TF_INTERNAL: TF_Code
TF_INVALID_ARGUMENT: TF_Code
TF_OK: TF_Code
TF_OUT_OF_RANGE: TF_Code
TF_PERMISSION_DENIED: TF_Code
TF_RESOURCE_EXHAUSTED: TF_Code
TF_UNAUTHENTICATED: TF_Code
TF_UNIMPLEMENTED: TF_Code
TF_UNKNOWN: TF_Code

class TF_Code:
    __members__: ClassVar[dict] = ...  # read-only
    TF_ABORTED: ClassVar[TF_Code] = ...
    TF_CANCELLED: ClassVar[TF_Code] = ...
    TF_DATA_LOSS: ClassVar[TF_Code] = ...
    TF_DEADLINE_EXCEEDED: ClassVar[TF_Code] = ...
    TF_FAILED_PRECONDITION: ClassVar[TF_Code] = ...
    TF_INTERNAL: ClassVar[TF_Code] = ...
    TF_INVALID_ARGUMENT: ClassVar[TF_Code] = ...
    TF_OK: ClassVar[TF_Code] = ...
    TF_OUT_OF_RANGE: ClassVar[TF_Code] = ...
    TF_PERMISSION_DENIED: ClassVar[TF_Code] = ...
    TF_RESOURCE_EXHAUSTED: ClassVar[TF_Code] = ...
    TF_UNAUTHENTICATED: ClassVar[TF_Code] = ...
    TF_UNIMPLEMENTED: ClassVar[TF_Code] = ...
    TF_UNKNOWN: ClassVar[TF_Code] = ...
    __entries: ClassVar[dict] = ...
    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

def PyExceptionRegistry_Init(arg0: object) -> None: ...
def PyExceptionRegistry_Lookup(arg0: TF_Code) -> None: ...
