# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_segmenter/proto/image_segmenter_graph_options.proto
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
from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.core.proto import base_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_base__options__pb2
from mediapipe.tasks.cc.vision.image_segmenter.proto import segmenter_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__segmenter_dot_proto_dot_segmenter__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nSmediapipe/tasks/cc/vision/image_segmenter/proto/image_segmenter_graph_options.proto\x12,mediapipe.tasks.vision.image_segmenter.proto\x1a$mediapipe/framework/calculator.proto\x1a,mediapipe/framework/calculator_options.proto\x1a\x30mediapipe/tasks/cc/core/proto/base_options.proto\x1aGmediapipe/tasks/cc/vision/image_segmenter/proto/segmenter_options.proto\"\xd1\x02\n\x1aImageSegmenterGraphOptions\x12=\n\x0c\x62\x61se_options\x18\x01 \x01(\x0b\x32\'.mediapipe.tasks.core.proto.BaseOptions\x12 \n\x14\x64isplay_names_locale\x18\x02 \x01(\t:\x02\x65n\x12Y\n\x11segmenter_options\x18\x03 \x01(\x0b\x32>.mediapipe.tasks.vision.image_segmenter.proto.SegmenterOptions2w\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x9e\xc7\xb8\xda\x01 \x01(\x0b\x32H.mediapipe.tasks.vision.image_segmenter.proto.ImageSegmenterGraphOptionsBY\n6com.google.mediapipe.tasks.vision.imagesegmenter.protoB\x1fImageSegmenterGraphOptionsProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.image_segmenter.proto.image_segmenter_graph_options_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_IMAGESEGMENTERGRAPHOPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n6com.google.mediapipe.tasks.vision.imagesegmenter.protoB\037ImageSegmenterGraphOptionsProto'
  _globals['_IMAGESEGMENTERGRAPHOPTIONS']._serialized_start=341
  _globals['_IMAGESEGMENTERGRAPHOPTIONS']._serialized_end=678
# @@protoc_insertion_point(module_scope)
