# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/genai/inference/proto/llm_params.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.tasks.cc.genai.inference.proto import prompt_template_pb2 as mediapipe_dot_tasks_dot_cc_dot_genai_dot_inference_dot_proto_dot_prompt__template__pb2
from mediapipe.tasks.cc.genai.inference.proto import transformer_params_pb2 as mediapipe_dot_tasks_dot_cc_dot_genai_dot_inference_dot_proto_dot_transformer__params__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9mediapipe/tasks/cc/genai/inference/proto/llm_params.proto\x12\x10odml.infra.proto\x1a>mediapipe/tasks/cc/genai/inference/proto/prompt_template.proto\x1a\x41mediapipe/tasks/cc/genai/inference/proto/transformer_params.proto\"\xdc\x05\n\rLlmParameters\x12G\n\x16transformer_parameters\x18\x01 \x01(\x0b\x32\'.odml.infra.proto.TransformerParameters\x12\x12\n\nvocab_size\x18\x02 \x01(\x05\x12\x18\n\x0estart_token_id\x18\x04 \x01(\x05H\x00\x12\x15\n\x0bstart_token\x18\x06 \x01(\tH\x00\x12\x13\n\x0bstop_tokens\x18\x05 \x03(\t\x12]\n\x1binput_output_normalizations\x18\x07 \x03(\x0e\x32\x38.odml.infra.proto.LlmParameters.InputOutputNormalization\x12\x39\n\x0fprompt_template\x18\x08 \x01(\x0b\x32 .odml.infra.proto.PromptTemplate\x12\x1d\n\x10num_draft_tokens\x18\t \x01(\x05H\x01\x88\x01\x01\x12\x1c\n\x0fuser_role_token\x18\x0b \x01(\tH\x02\x88\x01\x01\x12\x1e\n\x11system_role_token\x18\x0c \x01(\tH\x03\x88\x01\x01\x12\x1d\n\x10model_role_token\x18\r \x01(\tH\x04\x88\x01\x01\x12\x1b\n\x0e\x65nd_role_token\x18\x0e \x01(\tH\x05\x88\x01\x01\"s\n\x18InputOutputNormalization\x12&\n\"INPUT_OUTPUT_NORMALIZATION_UNKNOWN\x10\x00\x12/\n+INPUT_OUTPUT_NORMALIZATION_BYTES_TO_UNICODE\x10\x01\x42\x13\n\x11start_token_unionB\x13\n\x11_num_draft_tokensB\x12\n\x10_user_role_tokenB\x14\n\x12_system_role_tokenB\x13\n\x11_model_role_tokenB\x11\n\x0f_end_role_tokenJ\x04\x08\x03\x10\x04*\xc6\x02\n\x0cLlmModelType\x12\x1a\n\x16LLM_MODEL_TYPE_UNKNOWN\x10\x00\x12\x1f\n\x1bLLM_MODEL_TYPE_FALCON_RW_1B\x10\x05\x12\x1b\n\x17LLM_MODEL_TYPE_GEMMA_2B\x10\x06\x12\x1b\n\x17LLM_MODEL_TYPE_GEMMA_7B\x10\x0c\x12\x1c\n\x18LLM_MODEL_TYPE_GEMMA2_2B\x10\x12\x12#\n\x1fLLM_MODEL_TYPE_STABLELM_4E1T_3B\x10\x08\x12\x18\n\x14LLM_MODEL_TYPE_PHI_2\x10\x0b\x12\x1a\n\x16LLM_MODEL_TYPE_TF_LITE\x10\x64\"\x04\x08\x01\x10\x01\"\x04\x08\x02\x10\x02\"\x04\x08\x03\x10\x03\"\x04\x08\x04\x10\x04\"\x04\x08\x07\x10\x07\"\x04\x08\t\x10\t\"\x04\x08\n\x10\n\"\x04\x08\r\x10\r\"\x04\x08\x0e\x10\x0e\"\x04\x08\x0f\x10\x0f\"\x04\x08\x10\x10\x10\"\x04\x08\x11\x10\x11\x42\x31\n\x1b\x63om.google.odml.infra.protoB\x12LLMParametersProtob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.genai.inference.proto.llm_params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033com.google.odml.infra.protoB\022LLMParametersProto'
  _globals['_LLMMODELTYPE']._serialized_start=946
  _globals['_LLMMODELTYPE']._serialized_end=1272
  _globals['_LLMPARAMETERS']._serialized_start=211
  _globals['_LLMPARAMETERS']._serialized_end=943
  _globals['_LLMPARAMETERS_INPUTOUTPUTNORMALIZATION']._serialized_start=698
  _globals['_LLMPARAMETERS_INPUTOUTPUTNORMALIZATION']._serialized_end=813
# @@protoc_insertion_point(module_scope)
