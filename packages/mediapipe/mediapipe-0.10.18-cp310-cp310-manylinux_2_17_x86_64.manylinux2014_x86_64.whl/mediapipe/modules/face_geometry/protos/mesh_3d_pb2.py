# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/face_geometry/protos/mesh_3d.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4mediapipe/modules/face_geometry/protos/mesh_3d.proto\x12\x17mediapipe.face_geometry\"\xf9\x01\n\x06Mesh3d\x12?\n\x0bvertex_type\x18\x01 \x01(\x0e\x32*.mediapipe.face_geometry.Mesh3d.VertexType\x12\x45\n\x0eprimitive_type\x18\x02 \x01(\x0e\x32-.mediapipe.face_geometry.Mesh3d.PrimitiveType\x12\x15\n\rvertex_buffer\x18\x03 \x03(\x02\x12\x14\n\x0cindex_buffer\x18\x04 \x03(\r\"\x1b\n\nVertexType\x12\r\n\tVERTEX_PT\x10\x00\"\x1d\n\rPrimitiveType\x12\x0c\n\x08TRIANGLE\x10\x00\x42\x38\n)com.google.mediapipe.modules.facegeometryB\x0bMesh3dProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.modules.face_geometry.protos.mesh_3d_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n)com.google.mediapipe.modules.facegeometryB\013Mesh3dProto'
  _globals['_MESH3D']._serialized_start=82
  _globals['_MESH3D']._serialized_end=331
  _globals['_MESH3D_VERTEXTYPE']._serialized_start=273
  _globals['_MESH3D_VERTEXTYPE']._serialized_end=300
  _globals['_MESH3D_PRIMITIVETYPE']._serialized_start=302
  _globals['_MESH3D_PRIMITIVETYPE']._serialized_end=331
# @@protoc_insertion_point(module_scope)
