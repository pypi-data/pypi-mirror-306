# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_generator/proto/image_generator_graph_options.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.tasks.cc.core.proto import external_file_pb2 as mediapipe_dot_tasks_dot_cc_dot_core_dot_proto_dot_external__file__pb2
from mediapipe.tasks.cc.vision.image_generator.diffuser import stable_diffusion_iterate_calculator_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__generator_dot_diffuser_dot_stable__diffusion__iterate__calculator__pb2
from mediapipe.tasks.cc.vision.image_generator.proto import control_plugin_graph_options_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_image__generator_dot_proto_dot_control__plugin__graph__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nSmediapipe/tasks/cc/vision/image_generator/proto/image_generator_graph_options.proto\x12,mediapipe.tasks.vision.image_generator.proto\x1a\x31mediapipe/tasks/cc/core/proto/external_file.proto\x1a\\mediapipe/tasks/cc/vision/image_generator/diffuser/stable_diffusion_iterate_calculator.proto\x1aRmediapipe/tasks/cc/vision/image_generator/proto/control_plugin_graph_options.proto\"\xd3\x02\n\x1aImageGeneratorGraphOptions\x12\"\n\x1atext2image_model_directory\x18\x01 \x01(\t\x12\x43\n\x11lora_weights_file\x18\x02 \x01(\x0b\x32(.mediapipe.tasks.core.proto.ExternalFile\x12n\n\x1d\x63ontrol_plugin_graphs_options\x18\x03 \x03(\x0b\x32G.mediapipe.tasks.vision.image_generator.proto.ControlPluginGraphOptions\x12\\\n stable_diffusion_iterate_options\x18\x04 \x01(\x0b\x32\x32.mediapipe.StableDiffusionIterateCalculatorOptionsBY\n6com.google.mediapipe.tasks.vision.imagegenerator.protoB\x1fImageGeneratorGraphOptionsProtob\x06proto3')



_IMAGEGENERATORGRAPHOPTIONS = DESCRIPTOR.message_types_by_name['ImageGeneratorGraphOptions']
ImageGeneratorGraphOptions = _reflection.GeneratedProtocolMessageType('ImageGeneratorGraphOptions', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEGENERATORGRAPHOPTIONS,
  '__module__' : 'mediapipe.tasks.cc.vision.image_generator.proto.image_generator_graph_options_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.vision.image_generator.proto.ImageGeneratorGraphOptions)
  })
_sym_db.RegisterMessage(ImageGeneratorGraphOptions)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n6com.google.mediapipe.tasks.vision.imagegenerator.protoB\037ImageGeneratorGraphOptionsProto'
  _IMAGEGENERATORGRAPHOPTIONS._serialized_start=363
  _IMAGEGENERATORGRAPHOPTIONS._serialized_end=702
# @@protoc_insertion_point(module_scope)
