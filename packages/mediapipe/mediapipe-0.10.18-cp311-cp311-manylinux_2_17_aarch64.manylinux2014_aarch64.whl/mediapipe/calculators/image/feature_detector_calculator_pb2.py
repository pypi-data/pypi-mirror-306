# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/feature_detector_calculator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=mediapipe/calculators/image/feature_detector_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xe4\x01\n FeatureDetectorCalculatorOptions\x12\x14\n\x0coutput_patch\x18\x01 \x01(\x08\x12\x19\n\x0cmax_features\x18\x02 \x01(\x05:\x03\x32\x30\x30\x12\x18\n\rpyramid_level\x18\x03 \x01(\x05:\x01\x34\x12\x19\n\x0cscale_factor\x18\x04 \x01(\x02:\x03\x31.22Z\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb0\x85\xf5\x84\x01 \x01(\x0b\x32+.mediapipe.FeatureDetectorCalculatorOptions')



_FEATUREDETECTORCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['FeatureDetectorCalculatorOptions']
FeatureDetectorCalculatorOptions = _reflection.GeneratedProtocolMessageType('FeatureDetectorCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _FEATUREDETECTORCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.image.feature_detector_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.FeatureDetectorCalculatorOptions)
  })
_sym_db.RegisterMessage(FeatureDetectorCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_FEATUREDETECTORCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _FEATUREDETECTORCALCULATOROPTIONS._serialized_start=115
  _FEATUREDETECTORCALCULATOROPTIONS._serialized_end=343
# @@protoc_insertion_point(module_scope)
