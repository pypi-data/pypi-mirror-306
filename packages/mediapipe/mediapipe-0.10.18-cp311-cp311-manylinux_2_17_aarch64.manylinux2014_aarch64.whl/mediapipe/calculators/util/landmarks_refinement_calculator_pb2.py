# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/landmarks_refinement_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@mediapipe/calculators/util/landmarks_refinement_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xdd\x05\n$LandmarksRefinementCalculatorOptions\x12N\n\nrefinement\x18\x01 \x03(\x0b\x32:.mediapipe.LandmarksRefinementCalculatorOptions.Refinement\x1a\x11\n\x0fZRefinementNone\x1a\x11\n\x0fZRefinementCopy\x1a\x37\n\x18ZRefinementAssignAverage\x12\x1b\n\x13indexes_for_average\x18\x01 \x03(\x05\x1a\xab\x02\n\x0bZRefinement\x12O\n\x04none\x18\x01 \x01(\x0b\x32?.mediapipe.LandmarksRefinementCalculatorOptions.ZRefinementNoneH\x00\x12O\n\x04\x63opy\x18\x02 \x01(\x0b\x32?.mediapipe.LandmarksRefinementCalculatorOptions.ZRefinementCopyH\x00\x12\x62\n\x0e\x61ssign_average\x18\x03 \x01(\x0b\x32H.mediapipe.LandmarksRefinementCalculatorOptions.ZRefinementAssignAverageH\x00\x42\x16\n\x14z_refinement_options\x1ax\n\nRefinement\x12\x17\n\x0findexes_mapping\x18\x01 \x03(\x05\x12Q\n\x0cz_refinement\x18\x02 \x01(\x0b\x32;.mediapipe.LandmarksRefinementCalculatorOptions.ZRefinement2^\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xa2\x9c\x8e\xb6\x01 \x01(\x0b\x32/.mediapipe.LandmarksRefinementCalculatorOptions')



_LANDMARKSREFINEMENTCALCULATOROPTIONS = DESCRIPTOR.message_types_by_name['LandmarksRefinementCalculatorOptions']
_LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTNONE = _LANDMARKSREFINEMENTCALCULATOROPTIONS.nested_types_by_name['ZRefinementNone']
_LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTCOPY = _LANDMARKSREFINEMENTCALCULATOROPTIONS.nested_types_by_name['ZRefinementCopy']
_LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTASSIGNAVERAGE = _LANDMARKSREFINEMENTCALCULATOROPTIONS.nested_types_by_name['ZRefinementAssignAverage']
_LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENT = _LANDMARKSREFINEMENTCALCULATOROPTIONS.nested_types_by_name['ZRefinement']
_LANDMARKSREFINEMENTCALCULATOROPTIONS_REFINEMENT = _LANDMARKSREFINEMENTCALCULATOROPTIONS.nested_types_by_name['Refinement']
LandmarksRefinementCalculatorOptions = _reflection.GeneratedProtocolMessageType('LandmarksRefinementCalculatorOptions', (_message.Message,), {

  'ZRefinementNone' : _reflection.GeneratedProtocolMessageType('ZRefinementNone', (_message.Message,), {
    'DESCRIPTOR' : _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTNONE,
    '__module__' : 'mediapipe.calculators.util.landmarks_refinement_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.LandmarksRefinementCalculatorOptions.ZRefinementNone)
    })
  ,

  'ZRefinementCopy' : _reflection.GeneratedProtocolMessageType('ZRefinementCopy', (_message.Message,), {
    'DESCRIPTOR' : _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTCOPY,
    '__module__' : 'mediapipe.calculators.util.landmarks_refinement_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.LandmarksRefinementCalculatorOptions.ZRefinementCopy)
    })
  ,

  'ZRefinementAssignAverage' : _reflection.GeneratedProtocolMessageType('ZRefinementAssignAverage', (_message.Message,), {
    'DESCRIPTOR' : _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTASSIGNAVERAGE,
    '__module__' : 'mediapipe.calculators.util.landmarks_refinement_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.LandmarksRefinementCalculatorOptions.ZRefinementAssignAverage)
    })
  ,

  'ZRefinement' : _reflection.GeneratedProtocolMessageType('ZRefinement', (_message.Message,), {
    'DESCRIPTOR' : _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENT,
    '__module__' : 'mediapipe.calculators.util.landmarks_refinement_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.LandmarksRefinementCalculatorOptions.ZRefinement)
    })
  ,

  'Refinement' : _reflection.GeneratedProtocolMessageType('Refinement', (_message.Message,), {
    'DESCRIPTOR' : _LANDMARKSREFINEMENTCALCULATOROPTIONS_REFINEMENT,
    '__module__' : 'mediapipe.calculators.util.landmarks_refinement_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.LandmarksRefinementCalculatorOptions.Refinement)
    })
  ,
  'DESCRIPTOR' : _LANDMARKSREFINEMENTCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.util.landmarks_refinement_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.LandmarksRefinementCalculatorOptions)
  })
_sym_db.RegisterMessage(LandmarksRefinementCalculatorOptions)
_sym_db.RegisterMessage(LandmarksRefinementCalculatorOptions.ZRefinementNone)
_sym_db.RegisterMessage(LandmarksRefinementCalculatorOptions.ZRefinementCopy)
_sym_db.RegisterMessage(LandmarksRefinementCalculatorOptions.ZRefinementAssignAverage)
_sym_db.RegisterMessage(LandmarksRefinementCalculatorOptions.ZRefinement)
_sym_db.RegisterMessage(LandmarksRefinementCalculatorOptions.Refinement)

if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_LANDMARKSREFINEMENTCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _LANDMARKSREFINEMENTCALCULATOROPTIONS._serialized_start=118
  _LANDMARKSREFINEMENTCALCULATOROPTIONS._serialized_end=851
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTNONE._serialized_start=238
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTNONE._serialized_end=255
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTCOPY._serialized_start=257
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTCOPY._serialized_end=274
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTASSIGNAVERAGE._serialized_start=276
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENTASSIGNAVERAGE._serialized_end=331
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENT._serialized_start=334
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_ZREFINEMENT._serialized_end=633
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_REFINEMENT._serialized_start=635
  _LANDMARKSREFINEMENTCALCULATOROPTIONS_REFINEMENT._serialized_end=755
# @@protoc_insertion_point(module_scope)
