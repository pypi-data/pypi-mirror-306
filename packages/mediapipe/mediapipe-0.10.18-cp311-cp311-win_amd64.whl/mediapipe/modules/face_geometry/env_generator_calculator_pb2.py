# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/face_geometry/env_generator_calculator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.modules.face_geometry.protos import environment_pb2 as mediapipe_dot_modules_dot_face__geometry_dot_protos_dot_environment__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n>mediapipe/modules/face_geometry/env_generator_calculator.proto\x12\tmediapipe\x1a,mediapipe/framework/calculator_options.proto\x1a\x38mediapipe/modules/face_geometry/protos/environment.proto\"\xcb\x01\n)FaceGeometryEnvGeneratorCalculatorOptions\x12\x39\n\x0b\x65nvironment\x18\x01 \x01(\x0b\x32$.mediapipe.face_geometry.Environment2c\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf2\xd9\xac\x9a\x01 \x01(\x0b\x32\x34.mediapipe.FaceGeometryEnvGeneratorCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.modules.face_geometry.env_generator_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _globals['_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS']._serialized_start=182
  _globals['_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS']._serialized_end=385
# @@protoc_insertion_point(module_scope)
