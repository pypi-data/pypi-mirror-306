# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/face_geometry/geometry_pipeline_calculator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nBmediapipe/modules/face_geometry/geometry_pipeline_calculator.proto\x12\tmediapipe\x1a,mediapipe/framework/calculator_options.proto\"\x9f\x01\n%FaceGeometryPipelineCalculatorOptions\x12\x15\n\rmetadata_path\x18\x01 \x01(\t2_\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf4\xd9\xac\x9a\x01 \x01(\x0b\x32\x30.mediapipe.FaceGeometryPipelineCalculatorOptions')



_FACEGEOMETRYPIPELINECALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['FaceGeometryPipelineCalculatorOptions']
FaceGeometryPipelineCalculatorOptions = _reflection.GeneratedProtocolMessageType('FaceGeometryPipelineCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _FACEGEOMETRYPIPELINECALCULATOROPTIONS,
  '__module__' : 'mediapipe.modules.face_geometry.geometry_pipeline_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.FaceGeometryPipelineCalculatorOptions)
  })
_sym_db.RegisterMessage(FaceGeometryPipelineCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_FACEGEOMETRYPIPELINECALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _FACEGEOMETRYPIPELINECALCULATOROPTIONS._serialized_start=128
  _FACEGEOMETRYPIPELINECALCULATOROPTIONS._serialized_end=287
# @@protoc_insertion_point(module_scope)
