# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/components/processors/proto/classifier_options.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nGmediapipe/tasks/cc/components/processors/proto/classifier_options.proto\x12+mediapipe.tasks.components.processors.proto\"\x9e\x01\n\x11\x43lassifierOptions\x12 \n\x14\x64isplay_names_locale\x18\x01 \x01(\t:\x02\x65n\x12\x17\n\x0bmax_results\x18\x02 \x01(\x05:\x02-1\x12\x17\n\x0fscore_threshold\x18\x03 \x01(\x02\x12\x1a\n\x12\x63\x61tegory_allowlist\x18\x04 \x03(\t\x12\x19\n\x11\x63\x61tegory_denylist\x18\x05 \x03(\tBP\n6com.google.mediapipe.tasks.components.processors.protoB\x16\x43lassifierOptionsProto')



_CLASSIFIEROPTIONS = DESCRIPTOR.message_types_by_name['ClassifierOptions']
ClassifierOptions = _reflection.GeneratedProtocolMessageType('ClassifierOptions', (_message.Message,), {
  'DESCRIPTOR' : _CLASSIFIEROPTIONS,
  '__module__' : 'mediapipe.tasks.cc.components.processors.proto.classifier_options_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.components.processors.proto.ClassifierOptions)
  })
_sym_db.RegisterMessage(ClassifierOptions)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n6com.google.mediapipe.tasks.components.processors.protoB\026ClassifierOptionsProto'
  _CLASSIFIEROPTIONS._serialized_start=121
  _CLASSIFIEROPTIONS._serialized_end=279
# @@protoc_insertion_point(module_scope)
