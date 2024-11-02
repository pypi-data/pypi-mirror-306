# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tensor/tensors_to_classification_calculator.proto
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
from mediapipe.util import label_map_pb2 as mediapipe_dot_util_dot_label__map__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nGmediapipe/calculators/tensor/tensors_to_classification_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1emediapipe/util/label_map.proto\"\xc7\x05\n(TensorsToClassificationCalculatorOptions\x12\x1b\n\x13min_score_threshold\x18\x01 \x01(\x02\x12\r\n\x05top_k\x18\x02 \x01(\x05\x12 \n\x18sort_by_descending_score\x18\t \x01(\x08\x12\x16\n\x0elabel_map_path\x18\x03 \x01(\t\x12O\n\tlabel_map\x18\x05 \x01(\x0b\x32<.mediapipe.TensorsToClassificationCalculatorOptions.LabelMap\x12X\n\x0blabel_items\x18\x06 \x03(\x0b\x32\x43.mediapipe.TensorsToClassificationCalculatorOptions.LabelItemsEntry\x12\x1d\n\x15\x62inary_classification\x18\x04 \x01(\x08\x12\x1a\n\x0eignore_classes\x18\x07 \x03(\x05\x42\x02\x10\x01\x12\x19\n\rallow_classes\x18\x08 \x03(\x05\x42\x02\x10\x01\x1a\x83\x01\n\x08LabelMap\x12S\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x42.mediapipe.TensorsToClassificationCalculatorOptions.LabelMap.Entry\x1a\"\n\x05\x45ntry\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05label\x18\x02 \x01(\t\x1aJ\n\x0fLabelItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.mediapipe.LabelMapItem:\x02\x38\x01\x32\x62\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xae\x8d\x8c\xa0\x01 \x01(\x0b\x32\x33.mediapipe.TensorsToClassificationCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tensor.tensors_to_classification_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  _TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELITEMSENTRY._options = None
  _TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELITEMSENTRY._serialized_options = b'8\001'
  _TENSORSTOCLASSIFICATIONCALCULATOROPTIONS.fields_by_name['ignore_classes']._options = None
  _TENSORSTOCLASSIFICATIONCALCULATOROPTIONS.fields_by_name['ignore_classes']._serialized_options = b'\020\001'
  _TENSORSTOCLASSIFICATIONCALCULATOROPTIONS.fields_by_name['allow_classes']._options = None
  _TENSORSTOCLASSIFICATIONCALCULATOROPTIONS.fields_by_name['allow_classes']._serialized_options = b'\020\001'
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS']._serialized_start=157
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS']._serialized_end=868
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELMAP']._serialized_start=561
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELMAP']._serialized_end=692
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELMAP_ENTRY']._serialized_start=658
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELMAP_ENTRY']._serialized_end=692
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_start=694
  _globals['_TENSORSTOCLASSIFICATIONCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_end=768
# @@protoc_insertion_point(module_scope)
