# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/audio/spectrogram_calculator.proto
# Protobuf Python Version: 4.25.1
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8mediapipe/calculators/audio/spectrogram_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xb0\x06\n\x1cSpectrogramCalculatorOptions\x12\x1e\n\x16\x66rame_duration_seconds\x18\x01 \x01(\x01\x12 \n\x15\x66rame_overlap_seconds\x18\x02 \x01(\x01:\x01\x30\x12\x1e\n\x10pad_final_packet\x18\x03 \x01(\x08:\x04true\x12Z\n\x0boutput_type\x18\x04 \x01(\x0e\x32\x32.mediapipe.SpectrogramCalculatorOptions.OutputType:\x11SQUARED_MAGNITUDE\x12\'\n\x18\x61llow_multichannel_input\x18\x05 \x01(\x08:\x05\x66\x61lse\x12M\n\x0bwindow_type\x18\x06 \x01(\x0e\x32\x32.mediapipe.SpectrogramCalculatorOptions.WindowType:\x04HANN\x12\x17\n\x0coutput_scale\x18\x07 \x01(\x01:\x01\x31\x12\"\n\x13use_local_timestamp\x18\x08 \x01(\x08:\x05\x66\x61lse\x12\x13\n\x08\x66\x66t_size\x18\t \x01(\x05:\x01\x30\x12\x16\n\x0binput_scale\x18\n \x01(\x02:\x01\x31\x12Z\n\x12sample_buffer_mode\x18\x0b \x01(\x0e\x32\x38.mediapipe.SpectrogramCalculatorOptions.SampleBufferMode:\x04NONE\"T\n\nOutputType\x12\x15\n\x11SQUARED_MAGNITUDE\x10\x00\x12\x14\n\x10LINEAR_MAGNITUDE\x10\x01\x12\x0c\n\x08\x44\x45\x43IBELS\x10\x02\x12\x0b\n\x07\x43OMPLEX\x10\x03\">\n\nWindowType\x12\x08\n\x04HANN\x10\x00\x12\x0b\n\x07HAMMING\x10\x01\x12\n\n\x06\x43OSINE\x10\x02\x12\r\n\tSQRT_HANN\x10\x04\"\'\n\x10SampleBufferMode\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05RESET\x10\x01\x32U\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xc0\x88\xaa$ \x01(\x0b\x32\'.mediapipe.SpectrogramCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.audio.spectrogram_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SPECTROGRAMCALCULATOROPTIONS']._serialized_start=110
  _globals['_SPECTROGRAMCALCULATOROPTIONS']._serialized_end=926
  _globals['_SPECTROGRAMCALCULATOROPTIONS_OUTPUTTYPE']._serialized_start=650
  _globals['_SPECTROGRAMCALCULATOROPTIONS_OUTPUTTYPE']._serialized_end=734
  _globals['_SPECTROGRAMCALCULATOROPTIONS_WINDOWTYPE']._serialized_start=736
  _globals['_SPECTROGRAMCALCULATOROPTIONS_WINDOWTYPE']._serialized_end=798
  _globals['_SPECTROGRAMCALCULATOROPTIONS_SAMPLEBUFFERMODE']._serialized_start=800
  _globals['_SPECTROGRAMCALCULATOROPTIONS_SAMPLEBUFFERMODE']._serialized_end=839
# @@protoc_insertion_point(module_scope)
