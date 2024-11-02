# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/thread_pool_executor.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import mediapipe_options_pb2 as mediapipe_dot_framework_dot_mediapipe__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.mediapipe/framework/thread_pool_executor.proto\x12\tmediapipe\x1a+mediapipe/framework/mediapipe_options.proto\"\xe9\x02\n\x19ThreadPoolExecutorOptions\x12\x13\n\x0bnum_threads\x18\x01 \x01(\x05\x12\x12\n\nstack_size\x18\x02 \x01(\x05\x12\x1b\n\x13nice_priority_level\x18\x03 \x01(\x05\x12`\n\x1drequire_processor_performance\x18\x04 \x01(\x0e\x32\x39.mediapipe.ThreadPoolExecutorOptions.ProcessorPerformance\x12\x1a\n\x12thread_name_prefix\x18\x05 \x01(\t\"5\n\x14ProcessorPerformance\x12\n\n\x06NORMAL\x10\x00\x12\x07\n\x03LOW\x10\x01\x12\x08\n\x04HIGH\x10\x02\x32Q\n\x03\x65xt\x12\x1b.mediapipe.MediaPipeOptions\x18\x93\xd3\xf5J \x01(\x0b\x32$.mediapipe.ThreadPoolExecutorOptions')



_THREADPOOLEXECUTOROPTIONS = DESCRIPTOR.message_types_by_name['ThreadPoolExecutorOptions']
_THREADPOOLEXECUTOROPTIONS_PROCESSORPERFORMANCE = _THREADPOOLEXECUTOROPTIONS.enum_types_by_name['ProcessorPerformance']
ThreadPoolExecutorOptions = _reflection.GeneratedProtocolMessageType('ThreadPoolExecutorOptions', (_message.Message,), {
  'DESCRIPTOR' : _THREADPOOLEXECUTOROPTIONS,
  '__module__' : 'mediapipe.framework.thread_pool_executor_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.ThreadPoolExecutorOptions)
  })
_sym_db.RegisterMessage(ThreadPoolExecutorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_mediapipe__options__pb2.MediaPipeOptions.RegisterExtension(_THREADPOOLEXECUTOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _THREADPOOLEXECUTOROPTIONS._serialized_start=107
  _THREADPOOLEXECUTOROPTIONS._serialized_end=468
  _THREADPOOLEXECUTOROPTIONS_PROCESSORPERFORMANCE._serialized_start=332
  _THREADPOOLEXECUTOROPTIONS_PROCESSORPERFORMANCE._serialized_end=385
# @@protoc_insertion_point(module_scope)
