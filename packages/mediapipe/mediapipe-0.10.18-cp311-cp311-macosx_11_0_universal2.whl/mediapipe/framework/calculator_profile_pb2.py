# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/calculator_profile.proto
# Protobuf Python Version: 4.25.5
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,mediapipe/framework/calculator_profile.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"o\n\rTimeHistogram\x12\x10\n\x05total\x18\x01 \x01(\x03:\x01\x30\x12#\n\x12interval_size_usec\x18\x02 \x01(\x03:\x07\x31\x30\x30\x30\x30\x30\x30\x12\x18\n\rnum_intervals\x18\x03 \x01(\x03:\x01\x31\x12\r\n\x05\x63ount\x18\x04 \x03(\x03\"b\n\rStreamProfile\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x18\n\tback_edge\x18\x02 \x01(\x08:\x05\x66\x61lse\x12)\n\x07latency\x18\x03 \x01(\x0b\x32\x18.mediapipe.TimeHistogram\"\xb3\x02\n\x11\x43\x61lculatorProfile\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x17\n\x0copen_runtime\x18\x02 \x01(\x03:\x01\x30\x12\x18\n\rclose_runtime\x18\x03 \x01(\x03:\x01\x30\x12\x31\n\x0fprocess_runtime\x18\x04 \x01(\x0b\x32\x18.mediapipe.TimeHistogram\x12\x37\n\x15process_input_latency\x18\x05 \x01(\x0b\x32\x18.mediapipe.TimeHistogram\x12\x38\n\x16process_output_latency\x18\x06 \x01(\x0b\x32\x18.mediapipe.TimeHistogram\x12\x37\n\x15input_stream_profiles\x18\x07 \x03(\x0b\x32\x18.mediapipe.StreamProfile\"\xe1\x07\n\nGraphTrace\x12\x11\n\tbase_time\x18\x01 \x01(\x03\x12\x16\n\x0e\x62\x61se_timestamp\x18\x02 \x01(\x03\x12\x17\n\x0f\x63\x61lculator_name\x18\x03 \x03(\t\x12\x13\n\x0bstream_name\x18\x04 \x03(\t\x12?\n\x10\x63\x61lculator_trace\x18\x05 \x03(\x0b\x32%.mediapipe.GraphTrace.CalculatorTrace\x1a\x8e\x01\n\x0bStreamTrace\x12\x12\n\nstart_time\x18\x01 \x01(\x03\x12\x13\n\x0b\x66inish_time\x18\x02 \x01(\x03\x12\x18\n\x10packet_timestamp\x18\x03 \x01(\x03\x12\x11\n\tstream_id\x18\x04 \x01(\x05\x12\x15\n\tpacket_id\x18\x05 \x01(\x03\x42\x02\x18\x01\x12\x12\n\nevent_data\x18\x06 \x01(\x03\x1a\x9d\x02\n\x0f\x43\x61lculatorTrace\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x17\n\x0finput_timestamp\x18\x02 \x01(\x03\x12\x33\n\nevent_type\x18\x03 \x01(\x0e\x32\x1f.mediapipe.GraphTrace.EventType\x12\x12\n\nstart_time\x18\x04 \x01(\x03\x12\x13\n\x0b\x66inish_time\x18\x05 \x01(\x03\x12\x36\n\x0binput_trace\x18\x06 \x03(\x0b\x32!.mediapipe.GraphTrace.StreamTrace\x12\x37\n\x0coutput_trace\x18\x07 \x03(\x0b\x32!.mediapipe.GraphTrace.StreamTrace\x12\x11\n\tthread_id\x18\x08 \x01(\x05\"\x87\x03\n\tEventType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04OPEN\x10\x01\x12\x0b\n\x07PROCESS\x10\x02\x12\t\n\x05\x43LOSE\x10\x03\x12\r\n\tNOT_READY\x10\x04\x12\x15\n\x11READY_FOR_PROCESS\x10\x05\x12\x13\n\x0fREADY_FOR_CLOSE\x10\x06\x12\r\n\tTHROTTLED\x10\x07\x12\x0f\n\x0bUNTHROTTLED\x10\x08\x12\x11\n\rCPU_TASK_USER\x10\t\x12\x13\n\x0f\x43PU_TASK_SYSTEM\x10\n\x12\x0c\n\x08GPU_TASK\x10\x0b\x12\x0c\n\x08\x44SP_TASK\x10\x0c\x12\x0c\n\x08TPU_TASK\x10\r\x12\x13\n\x0fGPU_CALIBRATION\x10\x0e\x12\x11\n\rPACKET_QUEUED\x10\x0f\x12\x13\n\x0fGPU_TASK_INVOKE\x10\x10\x12\x13\n\x0fTPU_TASK_INVOKE\x10\x11\x12\x13\n\x0f\x43PU_TASK_INVOKE\x10\x12\x12\x1c\n\x18GPU_TASK_INVOKE_ADVANCED\x10\x13\x12\x19\n\x15TPU_TASK_INVOKE_ASYNC\x10\x14\"\xa7\x01\n\x0cGraphProfile\x12*\n\x0bgraph_trace\x18\x01 \x03(\x0b\x32\x15.mediapipe.GraphTrace\x12\x39\n\x13\x63\x61lculator_profiles\x18\x02 \x03(\x0b\x32\x1c.mediapipe.CalculatorProfile\x12\x30\n\x06\x63onfig\x18\x03 \x01(\x0b\x32 .mediapipe.CalculatorGraphConfigB4\n\x1a\x63om.google.mediapipe.protoB\x16\x43\x61lculatorProfileProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.framework.calculator_profile_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\032com.google.mediapipe.protoB\026CalculatorProfileProto'
  _globals['_GRAPHTRACE_STREAMTRACE'].fields_by_name['packet_id']._options = None
  _globals['_GRAPHTRACE_STREAMTRACE'].fields_by_name['packet_id']._serialized_options = b'\030\001'
  _globals['_TIMEHISTOGRAM']._serialized_start=97
  _globals['_TIMEHISTOGRAM']._serialized_end=208
  _globals['_STREAMPROFILE']._serialized_start=210
  _globals['_STREAMPROFILE']._serialized_end=308
  _globals['_CALCULATORPROFILE']._serialized_start=311
  _globals['_CALCULATORPROFILE']._serialized_end=618
  _globals['_GRAPHTRACE']._serialized_start=621
  _globals['_GRAPHTRACE']._serialized_end=1614
  _globals['_GRAPHTRACE_STREAMTRACE']._serialized_start=790
  _globals['_GRAPHTRACE_STREAMTRACE']._serialized_end=932
  _globals['_GRAPHTRACE_CALCULATORTRACE']._serialized_start=935
  _globals['_GRAPHTRACE_CALCULATORTRACE']._serialized_end=1220
  _globals['_GRAPHTRACE_EVENTTYPE']._serialized_start=1223
  _globals['_GRAPHTRACE_EVENTTYPE']._serialized_end=1614
  _globals['_GRAPHPROFILE']._serialized_start=1617
  _globals['_GRAPHPROFILE']._serialized_end=1784
# @@protoc_insertion_point(module_scope)
