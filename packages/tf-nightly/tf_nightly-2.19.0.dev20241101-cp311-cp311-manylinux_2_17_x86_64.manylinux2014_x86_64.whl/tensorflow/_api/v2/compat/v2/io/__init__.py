# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.io namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v2.io import gfile
from tensorflow.python.ops.gen_decode_proto_ops import decode_proto_v2 as decode_proto # line: 31
from tensorflow.python.ops.gen_encode_proto_ops import encode_proto # line: 27
from tensorflow.python.ops.gen_io_ops import matching_files # line: 391
from tensorflow.python.ops.gen_io_ops import write_file # line: 2269
from tensorflow.python.ops.gen_parsing_ops import decode_compressed # line: 144
from tensorflow.python.ops.gen_parsing_ops import parse_tensor # line: 2135
from tensorflow.python.ops.gen_string_ops import decode_base64 # line: 182
from tensorflow.python.ops.gen_string_ops import encode_base64 # line: 269
from tensorflow.python.framework.graph_io import write_graph # line: 28
from tensorflow.python.lib.io.tf_record import TFRecordOptions # line: 35
from tensorflow.python.lib.io.tf_record import TFRecordWriter # line: 211
from tensorflow.python.ops.image_ops_impl import decode_and_crop_jpeg # line: 3200
from tensorflow.python.ops.image_ops_impl import decode_bmp # line: 3206
from tensorflow.python.ops.image_ops_impl import decode_gif # line: 3211
from tensorflow.python.ops.image_ops_impl import decode_image # line: 3269
from tensorflow.python.ops.image_ops_impl import decode_jpeg # line: 3216
from tensorflow.python.ops.image_ops_impl import decode_png # line: 3221
from tensorflow.python.ops.image_ops_impl import encode_jpeg # line: 3227
from tensorflow.python.ops.image_ops_impl import encode_png # line: 3239
from tensorflow.python.ops.image_ops_impl import extract_jpeg_shape # line: 3232
from tensorflow.python.ops.image_ops_impl import is_jpeg # line: 3164
from tensorflow.python.ops.io_ops import read_file # line: 97
from tensorflow.python.ops.io_ops import serialize_tensor # line: 137
from tensorflow.python.ops.parsing_config import FixedLenFeature # line: 298
from tensorflow.python.ops.parsing_config import FixedLenSequenceFeature # line: 318
from tensorflow.python.ops.parsing_config import RaggedFeature # line: 54
from tensorflow.python.ops.parsing_config import SparseFeature # line: 223
from tensorflow.python.ops.parsing_config import VarLenFeature # line: 44
from tensorflow.python.ops.parsing_ops import decode_csv_v2 as decode_csv # line: 1070
from tensorflow.python.ops.parsing_ops import decode_json_example # line: 1149
from tensorflow.python.ops.parsing_ops import decode_raw # line: 840
from tensorflow.python.ops.parsing_ops import parse_example_v2 as parse_example # line: 71
from tensorflow.python.ops.parsing_ops import parse_sequence_example # line: 449
from tensorflow.python.ops.parsing_ops import parse_single_example_v2 as parse_single_example # line: 405
from tensorflow.python.ops.parsing_ops import parse_single_sequence_example # line: 693
from tensorflow.python.ops.sparse_ops import deserialize_many_sparse # line: 2356
from tensorflow.python.ops.sparse_ops import serialize_many_sparse_v2 as serialize_many_sparse # line: 2254
from tensorflow.python.ops.sparse_ops import serialize_sparse_v2 as serialize_sparse # line: 2197
from tensorflow.python.training.input import match_filenames_once # line: 56
