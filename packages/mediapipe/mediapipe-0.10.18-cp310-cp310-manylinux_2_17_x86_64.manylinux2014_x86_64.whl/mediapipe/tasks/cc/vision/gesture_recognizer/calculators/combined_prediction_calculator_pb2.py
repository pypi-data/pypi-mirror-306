# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/gesture_recognizer/calculators/combined_prediction_calculator.proto
# Protobuf Python Version: 4.25.1
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n]mediapipe/tasks/cc/vision/gesture_recognizer/calculators/combined_prediction_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xb9\x02\n#CombinedPredictionCalculatorOptions\x12\x43\n\x05\x63lass\x18\x01 \x03(\x0b\x32\x34.mediapipe.CombinedPredictionCalculatorOptions.Class\x12#\n\x18\x64\x65\x66\x61ult_global_threshold\x18\x02 \x01(\x02:\x01\x30\x12\x18\n\x10\x62\x61\x63kground_label\x18\x03 \x01(\t\x1a/\n\x05\x43lass\x12\r\n\x05label\x18\x01 \x01(\t\x12\x17\n\x0fscore_threshold\x18\x02 \x01(\x02\x32]\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x8b\x88\xd5\xe6\x01 \x01(\x0b\x32..mediapipe.CombinedPredictionCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.gesture_recognizer.calculators.combined_prediction_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_COMBINEDPREDICTIONCALCULATOROPTIONS']._serialized_start=147
  _globals['_COMBINEDPREDICTIONCALCULATOROPTIONS']._serialized_end=460
  _globals['_COMBINEDPREDICTIONCALCULATOROPTIONS_CLASS']._serialized_start=318
  _globals['_COMBINEDPREDICTIONCALCULATOROPTIONS_CLASS']._serialized_end=365
# @@protoc_insertion_point(module_scope)
