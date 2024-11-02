# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tflite/tflite_tensors_to_segmentation_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nLmediapipe/calculators/tflite/tflite_tensors_to_segmentation_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xbb\x02\n,TfLiteTensorsToSegmentationCalculatorOptions\x12\x14\n\x0ctensor_width\x18\x01 \x01(\x05\x12\x15\n\rtensor_height\x18\x02 \x01(\x05\x12\x17\n\x0ftensor_channels\x18\x03 \x01(\x05\x12&\n\x1b\x63ombine_with_previous_ratio\x18\x04 \x01(\x02:\x01\x31\x12\x1d\n\x12output_layer_index\x18\x05 \x01(\x05:\x01\x31\x12\x17\n\x0f\x66lip_vertically\x18\x06 \x01(\x08\x32\x65\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xca\xfb\xb4x \x01(\x0b\x32\x37.mediapipe.TfLiteTensorsToSegmentationCalculatorOptions')



_TFLITETENSORSTOSEGMENTATIONCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['TfLiteTensorsToSegmentationCalculatorOptions']
TfLiteTensorsToSegmentationCalculatorOptions = _reflection.GeneratedProtocolMessageType('TfLiteTensorsToSegmentationCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _TFLITETENSORSTOSEGMENTATIONCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.tflite.tflite_tensors_to_segmentation_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.TfLiteTensorsToSegmentationCalculatorOptions)
  })
_sym_db.RegisterMessage(TfLiteTensorsToSegmentationCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TFLITETENSORSTOSEGMENTATIONCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TFLITETENSORSTOSEGMENTATIONCALCULATOROPTIONS._serialized_start=130
  _TFLITETENSORSTOSEGMENTATIONCALCULATOROPTIONS._serialized_end=445
# @@protoc_insertion_point(module_scope)
