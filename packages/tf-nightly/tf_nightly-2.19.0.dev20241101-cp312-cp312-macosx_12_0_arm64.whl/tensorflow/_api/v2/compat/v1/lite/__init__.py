# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.lite namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.lite import constants
from tensorflow._api.v2.compat.v1.lite import experimental
from tensorflow.lite.python.convert import OpsSet # line: 153
from tensorflow.lite.python.convert import toco_convert # line: 932
from tensorflow.lite.python.interpreter import Interpreter # line: 348
from tensorflow.lite.python.lite import Optimize # line: 109
from tensorflow.lite.python.lite import RepresentativeDataset # line: 168
from tensorflow.lite.python.lite import TFLiteConverter # line: 2994
from tensorflow.lite.python.lite import TargetSpec # line: 192
from tensorflow.lite.python.lite import TocoConverter # line: 3370
from tensorflow.lite.python.op_hint import OpHint # line: 88

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "lite", public_apis=None, deprecation=False,
      has_lite=False)
