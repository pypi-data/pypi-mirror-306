# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: xla/service/metrics.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19xla/service/metrics.proto\x12\x03xla\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\",\n\x0eKeyValueMetric\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03\"\xbc\x01\n\x0bPassMetrics\x12\x11\n\tmodule_id\x18\x01 \x01(\x04\x12\x11\n\tpass_name\x18\x02 \x01(\t\x12\x30\n\rpass_duration\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\x12,\n\x0e\x63ustom_metrics\x18\x04 \x01(\x0b\x32\x14.google.protobuf.Any\x12\'\n\nkv_metrics\x18\x05 \x03(\x0b\x32\x13.xla.KeyValueMetric\"\xbd\x01\n\x07JobInfo\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04\x63\x65ll\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x11\n\x04user\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x10\n\x03uid\x18\x04 \x01(\x03H\x03\x88\x01\x01\x12\x14\n\x07task_id\x18\x05 \x01(\x03H\x04\x88\x01\x01\x12\x15\n\x08task_uid\x18\x06 \x01(\x03H\x05\x88\x01\x01\x42\x07\n\x05_nameB\x07\n\x05_cellB\x07\n\x05_userB\x06\n\x04_uidB\n\n\x08_task_idB\x0b\n\t_task_uid\"\x89\x03\n\x13\x43ompilationLogEntry\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x05stage\x18\x02 \x01(\x0e\x32).xla.CompilationLogEntry.CompilationStage\x12+\n\x08\x64uration\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x12\n\ntask_index\x18\x04 \x01(\x05\x12&\n\x0cpass_metrics\x18\x05 \x03(\x0b\x32\x10.xla.PassMetrics\x12\x12\n\nmodule_ids\x18\x06 \x03(\x04\x12\x1e\n\x08job_info\x18\x07 \x01(\x0b\x32\x0c.xla.JobInfo\"l\n\x10\x43ompilationStage\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0e\n\nEND_TO_END\x10\x01\x12\x0e\n\nHLO_PASSES\x10\x02\x12\x13\n\x0f\x43ODE_GENERATION\x10\x03\x12\x12\n\x0e\x42\x41\x43KEND_PASSES\x10\x04\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'xla.service.metrics_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _KEYVALUEMETRIC._serialized_start=126
  _KEYVALUEMETRIC._serialized_end=170
  _PASSMETRICS._serialized_start=173
  _PASSMETRICS._serialized_end=361
  _JOBINFO._serialized_start=364
  _JOBINFO._serialized_end=553
  _COMPILATIONLOGENTRY._serialized_start=556
  _COMPILATIONLOGENTRY._serialized_end=949
  _COMPILATIONLOGENTRY_COMPILATIONSTAGE._serialized_start=841
  _COMPILATIONLOGENTRY_COMPILATIONSTAGE._serialized_end=949
# @@protoc_insertion_point(module_scope)
