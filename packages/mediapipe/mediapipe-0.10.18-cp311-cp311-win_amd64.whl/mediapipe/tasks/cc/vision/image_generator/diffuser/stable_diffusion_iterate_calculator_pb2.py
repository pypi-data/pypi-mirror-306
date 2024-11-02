# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/image_generator/diffuser/stable_diffusion_iterate_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\\mediapipe/tasks/cc/vision/image_generator/diffuser/stable_diffusion_iterate_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xfe\x06\n\'StableDiffusionIterateCalculatorOptions\x12\x14\n\tbase_seed\x18\x01 \x01(\r:\x01\x30\x12\x1f\n\x12output_image_width\x18\x02 \x01(\x05:\x03\x35\x31\x32\x12 \n\x13output_image_height\x18\x03 \x01(\x05:\x03\x35\x31\x32\x12\x1a\n\x0b\x66ile_folder\x18\x04 \x01(\t:\x05\x62ins/\x12\x1a\n\x10lora_file_folder\x18\t \x01(\t:\x00\x12s\n\x1alora_weights_layer_mapping\x18\n \x03(\x0b\x32O.mediapipe.StableDiffusionIterateCalculatorOptions.LoraWeightsLayerMappingEntry\x12\x14\n\tlora_rank\x18\x0c \x01(\x05:\x01\x34\x12!\n\x16show_every_n_iteration\x18\x05 \x01(\x05:\x01\x31\x12 \n\x11\x65mit_empty_packet\x18\x06 \x01(\x08:\x05\x66\x61lse\x12[\n\x10\x63l_priority_hint\x18\x07 \x01(\x0e\x32\x41.mediapipe.StableDiffusionIterateCalculatorOptions.ClPriorityHint\x12V\n\nmodel_type\x18\x08 \x01(\x0e\x32<.mediapipe.StableDiffusionIterateCalculatorOptions.ModelType:\x04SD_1\x12\x1b\n\x10plugins_strength\x18\x0b \x01(\x02:\x01\x31\x1a>\n\x1cLoraWeightsLayerMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x04:\x02\x38\x01\"Y\n\x0e\x43lPriorityHint\x12\x18\n\x14PRIORITY_HINT_NORMAL\x10\x00\x12\x15\n\x11PRIORITY_HINT_LOW\x10\x01\x12\x16\n\x12PRIORITY_HINT_HIGH\x10\x02\"\"\n\tModelType\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x08\n\x04SD_1\x10\x01\x32\x61\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x9c\x95\xcc\xf3\x01 \x01(\x0b\x32\x32.mediapipe.StableDiffusionIterateCalculatorOptionsBU\n%com.google.mediapipe.calculator.protoB,StableDiffusionIterateCalculatorOptionsProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.image_generator.diffuser.stable_diffusion_iterate_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_STABLEDIFFUSIONITERATECALCULATOROPTIONS.extensions_by_name['ext'])

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.google.mediapipe.calculator.protoB,StableDiffusionIterateCalculatorOptionsProto'
  _STABLEDIFFUSIONITERATECALCULATOROPTIONS_LORAWEIGHTSLAYERMAPPINGENTRY._options = None
  _STABLEDIFFUSIONITERATECALCULATOROPTIONS_LORAWEIGHTSLAYERMAPPINGENTRY._serialized_options = b'8\001'
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS']._serialized_start=146
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS']._serialized_end=1040
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS_LORAWEIGHTSLAYERMAPPINGENTRY']._serialized_start=752
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS_LORAWEIGHTSLAYERMAPPINGENTRY']._serialized_end=814
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS_CLPRIORITYHINT']._serialized_start=816
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS_CLPRIORITYHINT']._serialized_end=905
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS_MODELTYPE']._serialized_start=907
  _globals['_STABLEDIFFUSIONITERATECALCULATOROPTIONS_MODELTYPE']._serialized_end=941
# @@protoc_insertion_point(module_scope)
