# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/core/packet_cloner_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9mediapipe/calculators/core/packet_cloner_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xe9\x01\n\x1dPacketClonerCalculatorOptions\x12\x33\n$output_only_when_all_inputs_received\x18\x01 \x01(\x08:\x05\x66\x61lse\x12;\n,output_packets_only_when_all_inputs_received\x18\x02 \x01(\x08:\x05\x66\x61lse2V\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x95\xa6\xb8{ \x01(\x0b\x32(.mediapipe.PacketClonerCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.core.packet_cloner_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_PACKETCLONERCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _globals['_PACKETCLONERCALCULATOROPTIONS']._serialized_start=111
  _globals['_PACKETCLONERCALCULATOROPTIONS']._serialized_end=344
# @@protoc_insertion_point(module_scope)
