# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/tone_models.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)mediapipe/util/tracking/tone_models.proto\x12\tmediapipe\"\x87\x01\n\rGainBiasModel\x12\x12\n\x07gain_c1\x18\x01 \x01(\x02:\x01\x31\x12\x12\n\x07\x62ias_c1\x18\x02 \x01(\x02:\x01\x30\x12\x12\n\x07gain_c2\x18\x03 \x01(\x02:\x01\x31\x12\x12\n\x07\x62ias_c2\x18\x04 \x01(\x02:\x01\x30\x12\x12\n\x07gain_c3\x18\x05 \x01(\x02:\x01\x31\x12\x12\n\x07\x62ias_c3\x18\x06 \x01(\x02:\x01\x30\"?\n\x14MixtureGainBiasModel\x12\'\n\x05model\x18\x01 \x03(\x0b\x32\x18.mediapipe.GainBiasModel\"\xdd\x01\n\x0f\x41\x66\x66ineToneModel\x12\x0f\n\x04g_00\x18\x01 \x01(\x02:\x01\x31\x12\x0f\n\x04g_01\x18\x02 \x01(\x02:\x01\x30\x12\x0f\n\x04g_02\x18\x03 \x01(\x02:\x01\x30\x12\x0f\n\x04g_03\x18\x04 \x01(\x02:\x01\x30\x12\x0f\n\x04g_10\x18\x05 \x01(\x02:\x01\x30\x12\x0f\n\x04g_11\x18\x06 \x01(\x02:\x01\x31\x12\x0f\n\x04g_12\x18\x07 \x01(\x02:\x01\x30\x12\x0f\n\x04g_13\x18\x08 \x01(\x02:\x01\x30\x12\x0f\n\x04g_20\x18\t \x01(\x02:\x01\x30\x12\x0f\n\x04g_21\x18\n \x01(\x02:\x01\x30\x12\x0f\n\x04g_22\x18\x0b \x01(\x02:\x01\x31\x12\x0f\n\x04g_23\x18\x0c \x01(\x02:\x01\x30\"C\n\x16MixtureAffineToneModel\x12)\n\x05model\x18\x01 \x03(\x0b\x32\x1a.mediapipe.AffineToneModel')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.tracking.tone_models_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_GAINBIASMODEL']._serialized_start=57
  _globals['_GAINBIASMODEL']._serialized_end=192
  _globals['_MIXTUREGAINBIASMODEL']._serialized_start=194
  _globals['_MIXTUREGAINBIASMODEL']._serialized_end=257
  _globals['_AFFINETONEMODEL']._serialized_start=260
  _globals['_AFFINETONEMODEL']._serialized_end=481
  _globals['_MIXTUREAFFINETONEMODEL']._serialized_start=483
  _globals['_MIXTUREAFFINETONEMODEL']._serialized_end=550
# @@protoc_insertion_point(module_scope)
