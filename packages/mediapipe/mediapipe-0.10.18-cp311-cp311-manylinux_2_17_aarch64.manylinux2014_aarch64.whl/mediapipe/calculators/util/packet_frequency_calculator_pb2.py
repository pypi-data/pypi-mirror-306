# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/packet_frequency_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<mediapipe/calculators/util/packet_frequency_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xa8\x01\n PacketFrequencyCalculatorOptions\x12\x1a\n\x0ftime_window_sec\x18\x01 \x01(\x01:\x01\x33\x12\r\n\x05label\x18\x02 \x03(\t2Y\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb6\xc3\xaaP \x01(\x0b\x32+.mediapipe.PacketFrequencyCalculatorOptions')



_PACKETFREQUENCYCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['PacketFrequencyCalculatorOptions']
PacketFrequencyCalculatorOptions = _reflection.GeneratedProtocolMessageType('PacketFrequencyCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _PACKETFREQUENCYCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.util.packet_frequency_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.PacketFrequencyCalculatorOptions)
  })
_sym_db.RegisterMessage(PacketFrequencyCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_PACKETFREQUENCYCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _PACKETFREQUENCYCALCULATOROPTIONS._serialized_start=114
  _PACKETFREQUENCYCALCULATOROPTIONS._serialized_end=282
# @@protoc_insertion_point(module_scope)
