# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/components/processors/proto/detection_postprocessing_graph_options.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.calculators.tensor import tensors_to_detections_calculator_pb2 as mediapipe_dot_calculators_dot_tensor_dot_tensors__to__detections__calculator__pb2
from mediapipe.calculators.tflite import ssd_anchors_calculator_pb2 as mediapipe_dot_calculators_dot_tflite_dot_ssd__anchors__calculator__pb2
from mediapipe.calculators.util import detection_label_id_to_text_calculator_pb2 as mediapipe_dot_calculators_dot_util_dot_detection__label__id__to__text__calculator__pb2
from mediapipe.calculators.util import non_max_suppression_calculator_pb2 as mediapipe_dot_calculators_dot_util_dot_non__max__suppression__calculator__pb2
from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2
from mediapipe.tasks.cc.components.calculators import score_calibration_calculator_pb2 as mediapipe_dot_tasks_dot_cc_dot_components_dot_calculators_dot_score__calibration__calculator__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n[mediapipe/tasks/cc/components/processors/proto/detection_postprocessing_graph_options.proto\x12+mediapipe.tasks.components.processors.proto\x1a\x43mediapipe/calculators/tensor/tensors_to_detections_calculator.proto\x1a\x39mediapipe/calculators/tflite/ssd_anchors_calculator.proto\x1a\x46mediapipe/calculators/util/detection_label_id_to_text_calculator.proto\x1a?mediapipe/calculators/util/non_max_suppression_calculator.proto\x1a$mediapipe/framework/calculator.proto\x1aLmediapipe/tasks/cc/components/calculators/score_calibration_calculator.proto\"\xc5\x05\n#DetectionPostprocessingGraphOptions\x12H\n\x13ssd_anchors_options\x18\x01 \x01(\x0b\x32&.mediapipe.SsdAnchorsCalculatorOptionsH\x00\x88\x01\x01\x12[\n\x1dtensors_to_detections_options\x18\x02 \x01(\x0b\x32/.mediapipe.TensorsToDetectionsCalculatorOptionsH\x01\x88\x01\x01\x12W\n\x1bnon_max_suppression_options\x18\x03 \x01(\x0b\x32-.mediapipe.NonMaxSuppressionCalculatorOptionsH\x02\x88\x01\x01\x12Z\n\x19score_calibration_options\x18\x04 \x01(\x0b\x32\x32.mediapipe.tasks.ScoreCalibrationCalculatorOptionsH\x03\x88\x01\x01\x12\x64\n#detection_label_ids_to_text_options\x18\x05 \x01(\x0b\x32\x32.mediapipe.DetectionLabelIdToTextCalculatorOptionsH\x04\x88\x01\x01\x12\"\n\x15has_quantized_outputs\x18\x06 \x01(\x08H\x05\x88\x01\x01\x42\x16\n\x14_ssd_anchors_optionsB \n\x1e_tensors_to_detections_optionsB\x1e\n\x1c_non_max_suppression_optionsB\x1c\n\x1a_score_calibration_optionsB&\n$_detection_label_ids_to_text_optionsB\x18\n\x16_has_quantized_outputsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.components.processors.proto.detection_postprocessing_graph_options_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_DETECTIONPOSTPROCESSINGGRAPHOPTIONS']._serialized_start=522
  _globals['_DETECTIONPOSTPROCESSINGGRAPHOPTIONS']._serialized_end=1231
# @@protoc_insertion_point(module_scope)
