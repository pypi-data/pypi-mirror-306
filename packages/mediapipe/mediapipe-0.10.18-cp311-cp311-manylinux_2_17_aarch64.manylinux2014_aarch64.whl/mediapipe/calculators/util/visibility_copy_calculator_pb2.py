# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/visibility_copy_calculator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;mediapipe/calculators/util/visibility_copy_calculator.proto\x12\tmediapipe\x1a,mediapipe/framework/calculator_options.proto\"\xb8\x01\n\x1fVisibilityCopyCalculatorOptions\x12\x1d\n\x0f\x63opy_visibility\x18\x01 \x01(\x08:\x04true\x12\x1b\n\rcopy_presence\x18\x02 \x01(\x08:\x04true2Y\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xa5\x9c\xb8\xad\x01 \x01(\x0b\x32*.mediapipe.VisibilityCopyCalculatorOptions')



_VISIBILITYCOPYCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['VisibilityCopyCalculatorOptions']
VisibilityCopyCalculatorOptions = _reflection.GeneratedProtocolMessageType('VisibilityCopyCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _VISIBILITYCOPYCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.util.visibility_copy_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.VisibilityCopyCalculatorOptions)
  })
_sym_db.RegisterMessage(VisibilityCopyCalculatorOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_VISIBILITYCOPYCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _VISIBILITYCOPYCALCULATOROPTIONS._serialized_start=121
  _VISIBILITYCOPYCALCULATOROPTIONS._serialized_end=305
# @@protoc_insertion_point(module_scope)
