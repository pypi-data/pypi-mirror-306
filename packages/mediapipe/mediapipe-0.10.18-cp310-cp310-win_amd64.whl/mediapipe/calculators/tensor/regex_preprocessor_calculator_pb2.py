# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tensor/regex_preprocessor_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@mediapipe/calculators/tensor/regex_preprocessor_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\x97\x01\n\"RegexPreprocessorCalculatorOptions\x12\x13\n\x0bmax_seq_len\x18\x01 \x01(\x05\x32\\\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xd9\x82\x8f\xdd\x01 \x01(\x0b\x32-.mediapipe.RegexPreprocessorCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tensor.regex_preprocessor_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_REGEXPREPROCESSORCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _globals['_REGEXPREPROCESSORCALCULATOROPTIONS']._serialized_start=118
  _globals['_REGEXPREPROCESSORCALCULATOROPTIONS']._serialized_end=269
# @@protoc_insertion_point(module_scope)
