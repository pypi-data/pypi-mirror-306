# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/matrix_data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-mediapipe/framework/formats/matrix_data.proto\x12\tmediapipe\"\xa8\x01\n\nMatrixData\x12\x0c\n\x04rows\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ols\x18\x02 \x01(\x05\x12\x17\n\x0bpacked_data\x18\x03 \x03(\x02\x42\x02\x10\x01\x12:\n\x06layout\x18\x04 \x01(\x0e\x32\x1c.mediapipe.MatrixData.Layout:\x0c\x43OLUMN_MAJOR\")\n\x06Layout\x12\x10\n\x0c\x43OLUMN_MAJOR\x10\x00\x12\r\n\tROW_MAJOR\x10\x01\x42\x35\n\"com.google.mediapipe.formats.protoB\x0fMatrixDataProto')



_MATRIXDATA = DESCRIPTOR.message_types_by_name['MatrixData']
_MATRIXDATA_LAYOUT = _MATRIXDATA.enum_types_by_name['Layout']
MatrixData = _reflection.GeneratedProtocolMessageType('MatrixData', (_message.Message,), {
  'DESCRIPTOR' : _MATRIXDATA,
  '__module__' : 'mediapipe.framework.formats.matrix_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.MatrixData)
  })
_sym_db.RegisterMessage(MatrixData)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.google.mediapipe.formats.protoB\017MatrixDataProto'
  _MATRIXDATA.fields_by_name['packed_data']._options = None
  _MATRIXDATA.fields_by_name['packed_data']._serialized_options = b'\020\001'
  _MATRIXDATA._serialized_start=61
  _MATRIXDATA._serialized_end=229
  _MATRIXDATA_LAYOUT._serialized_start=188
  _MATRIXDATA_LAYOUT._serialized_end=229
# @@protoc_insertion_point(module_scope)
