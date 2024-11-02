# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/core/packet_thinner_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:mediapipe/calculators/core/packet_thinner_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xf3\x02\n\x1ePacketThinnerCalculatorOptions\x12R\n\x0cthinner_type\x18\x01 \x01(\x0e\x32\x35.mediapipe.PacketThinnerCalculatorOptions.ThinnerType:\x05\x41SYNC\x12\x11\n\x06period\x18\x02 \x01(\x03:\x01\x31\x12\x12\n\nstart_time\x18\x03 \x01(\x03\x12\x10\n\x08\x65nd_time\x18\x04 \x01(\x03\x12$\n\x16sync_output_timestamps\x18\x05 \x01(\x08:\x04true\x12 \n\x11update_frame_rate\x18\x06 \x01(\x08:\x05\x66\x61lse\"\"\n\x0bThinnerType\x12\t\n\x05\x41SYNC\x10\x01\x12\x08\n\x04SYNC\x10\x02\x32X\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x84\xd8\xca\x89\x01 \x01(\x0b\x32).mediapipe.PacketThinnerCalculatorOptions')



_PACKETTHINNERCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['PacketThinnerCalculatorOptions']
_PACKETTHINNERCALCULATOROPTIONS_THINNERTYPE = _PACKETTHINNERCALCULATOROPTIONS.enum_types_by_name['ThinnerType']
PacketThinnerCalculatorOptions = _reflection.GeneratedProtocolMessageType('PacketThinnerCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _PACKETTHINNERCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.core.packet_thinner_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.PacketThinnerCalculatorOptions)
  })
_sym_db.RegisterMessage(PacketThinnerCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_PACKETTHINNERCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _PACKETTHINNERCALCULATOROPTIONS._serialized_start=112
  _PACKETTHINNERCALCULATOROPTIONS._serialized_end=483
  _PACKETTHINNERCALCULATOROPTIONS_THINNERTYPE._serialized_start=359
  _PACKETTHINNERCALCULATOROPTIONS_THINNERTYPE._serialized_end=393
# @@protoc_insertion_point(module_scope)
