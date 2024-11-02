# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tensor/tensors_to_segmentation_calculator.proto
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
from mediapipe.gpu import gpu_origin_pb2 as mediapipe_dot_gpu_dot_gpu__origin__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nEmediapipe/calculators/tensor/tensors_to_segmentation_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1emediapipe/gpu/gpu_origin.proto\"\xe2\x02\n&TensorsToSegmentationCalculatorOptions\x12-\n\ngpu_origin\x18\x01 \x01(\x0e\x32\x19.mediapipe.GpuOrigin.Mode\x12V\n\nactivation\x18\x02 \x01(\x0e\x32<.mediapipe.TensorsToSegmentationCalculatorOptions.Activation:\x04NONE\x12\x1d\n\x12output_layer_index\x18\x03 \x01(\x05:\x01\x31\"0\n\nActivation\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07SIGMOID\x10\x01\x12\x0b\n\x07SOFTMAX\x10\x02\x32`\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xc2\x91\xbe\xb2\x01 \x01(\x0b\x32\x31.mediapipe.TensorsToSegmentationCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tensor.tensors_to_segmentation_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TENSORSTOSEGMENTATIONCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS']._serialized_start=155
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS']._serialized_end=509
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS_ACTIVATION']._serialized_start=363
  _globals['_TENSORSTOSEGMENTATIONCALCULATOROPTIONS_ACTIVATION']._serialized_end=411
# @@protoc_insertion_point(module_scope)
