# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/test_calculators.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*mediapipe/framework/test_calculators.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xdd\x01\n\x1dRandomMatrixCalculatorOptions\x12\x0c\n\x04rows\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ols\x18\x02 \x01(\x05\x12\x17\n\x0fstart_timestamp\x18\x03 \x01(\x03\x12\x17\n\x0flimit_timestamp\x18\x04 \x01(\x03\x12\x16\n\x0etimestamp_step\x18\x05 \x01(\x03\x32V\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xc8\xa0\xe9\x18 \x01(\x0b\x32(.mediapipe.RandomMatrixCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.framework.test_calculators_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_RANDOMMATRIXCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _globals['_RANDOMMATRIXCALCULATOROPTIONS']._serialized_start=96
  _globals['_RANDOMMATRIXCALCULATOROPTIONS']._serialized_end=317
# @@protoc_insertion_point(module_scope)
