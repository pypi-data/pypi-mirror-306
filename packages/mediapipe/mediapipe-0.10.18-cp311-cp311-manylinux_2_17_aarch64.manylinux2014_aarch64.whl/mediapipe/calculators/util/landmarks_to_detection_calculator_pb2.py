# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/landmarks_to_detection_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nBmediapipe/calculators/util/landmarks_to_detection_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xaa\x01\n%LandmarksToDetectionCalculatorOptions\x12!\n\x19selected_landmark_indices\x18\x01 \x03(\x05\x32^\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf5\xa9\x89| \x01(\x0b\x32\x30.mediapipe.LandmarksToDetectionCalculatorOptions')



_LANDMARKSTODETECTIONCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['LandmarksToDetectionCalculatorOptions']
LandmarksToDetectionCalculatorOptions = _reflection.GeneratedProtocolMessageType('LandmarksToDetectionCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _LANDMARKSTODETECTIONCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.util.landmarks_to_detection_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.LandmarksToDetectionCalculatorOptions)
  })
_sym_db.RegisterMessage(LandmarksToDetectionCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_LANDMARKSTODETECTIONCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _LANDMARKSTODETECTIONCALCULATOROPTIONS._serialized_start=120
  _LANDMARKSTODETECTIONCALCULATOROPTIONS._serialized_end=290
# @@protoc_insertion_point(module_scope)
