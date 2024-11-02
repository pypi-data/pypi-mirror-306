# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/objectron/calculators/annotation_data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.modules.objectron.calculators import a_r_capture_metadata_pb2 as mediapipe_dot_modules_dot_objectron_dot_calculators_dot_a__r__capture__metadata__pb2
from mediapipe.modules.objectron.calculators import object_pb2 as mediapipe_dot_modules_dot_objectron_dot_calculators_dot_object__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=mediapipe/modules/objectron/calculators/annotation_data.proto\x12\tmediapipe\x1a\x42mediapipe/modules/objectron/calculators/a_r_capture_metadata.proto\x1a\x34mediapipe/modules/objectron/calculators/object.proto\"8\n\x11NormalizedPoint2D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\r\n\x05\x64\x65pth\x18\x03 \x01(\x02\"*\n\x07Point3D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"\x85\x01\n\x11\x41nnotatedKeyPoint\x12\n\n\x02id\x18\x01 \x01(\x05\x12$\n\x08point_3d\x18\x02 \x01(\x0b\x32\x12.mediapipe.Point3D\x12.\n\x08point_2d\x18\x03 \x01(\x0b\x32\x1c.mediapipe.NormalizedPoint2D\x12\x0e\n\x06hidden\x18\x04 \x01(\x08\"\xa0\x01\n\x10ObjectAnnotation\x12\x11\n\tobject_id\x18\x01 \x01(\x05\x12/\n\tkeypoints\x18\x02 \x03(\x0b\x32\x1c.mediapipe.AnnotatedKeyPoint\x12\x12\n\nvisibility\x18\x03 \x01(\x02\x12\x10\n\x08rotation\x18\x04 \x03(\x02\x12\x13\n\x0btranslation\x18\x05 \x03(\x02\x12\r\n\x05scale\x18\x06 \x03(\x02\"\xb9\x01\n\x0f\x46rameAnnotation\x12\x10\n\x08\x66rame_id\x18\x01 \x01(\x05\x12\x30\n\x0b\x61nnotations\x18\x02 \x03(\x0b\x32\x1b.mediapipe.ObjectAnnotation\x12#\n\x06\x63\x61mera\x18\x03 \x01(\x0b\x32\x13.mediapipe.ARCamera\x12\x11\n\ttimestamp\x18\x04 \x01(\x01\x12\x14\n\x0cplane_center\x18\x05 \x03(\x02\x12\x14\n\x0cplane_normal\x18\x06 \x03(\x02\"e\n\x08Sequence\x12\"\n\x07objects\x18\x01 \x03(\x0b\x32\x11.mediapipe.Object\x12\x35\n\x11\x66rame_annotations\x18\x02 \x03(\x0b\x32\x1a.mediapipe.FrameAnnotationb\x06proto3')



_NORMALIZEDPOINT2D = DESCRIPTOR.message_types_by_name['NormalizedPoint2D']
_POINT3D = DESCRIPTOR.message_types_by_name['Point3D']
_ANNOTATEDKEYPOINT = DESCRIPTOR.message_types_by_name['AnnotatedKeyPoint']
_OBJECTANNOTATION = DESCRIPTOR.message_types_by_name['ObjectAnnotation']
_FRAMEANNOTATION = DESCRIPTOR.message_types_by_name['FrameAnnotation']
_SEQUENCE = DESCRIPTOR.message_types_by_name['Sequence']
NormalizedPoint2D = _reflection.GeneratedProtocolMessageType('NormalizedPoint2D', (_message.Message,), {
  'DESCRIPTOR' : _NORMALIZEDPOINT2D,
  '__module__' : 'mediapipe.modules.objectron.calculators.annotation_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.NormalizedPoint2D)
  })
_sym_db.RegisterMessage(NormalizedPoint2D)

Point3D = _reflection.GeneratedProtocolMessageType('Point3D', (_message.Message,), {
  'DESCRIPTOR' : _POINT3D,
  '__module__' : 'mediapipe.modules.objectron.calculators.annotation_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.Point3D)
  })
_sym_db.RegisterMessage(Point3D)

AnnotatedKeyPoint = _reflection.GeneratedProtocolMessageType('AnnotatedKeyPoint', (_message.Message,), {
  'DESCRIPTOR' : _ANNOTATEDKEYPOINT,
  '__module__' : 'mediapipe.modules.objectron.calculators.annotation_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.AnnotatedKeyPoint)
  })
_sym_db.RegisterMessage(AnnotatedKeyPoint)

ObjectAnnotation = _reflection.GeneratedProtocolMessageType('ObjectAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _OBJECTANNOTATION,
  '__module__' : 'mediapipe.modules.objectron.calculators.annotation_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.ObjectAnnotation)
  })
_sym_db.RegisterMessage(ObjectAnnotation)

FrameAnnotation = _reflection.GeneratedProtocolMessageType('FrameAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _FRAMEANNOTATION,
  '__module__' : 'mediapipe.modules.objectron.calculators.annotation_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.FrameAnnotation)
  })
_sym_db.RegisterMessage(FrameAnnotation)

Sequence = _reflection.GeneratedProtocolMessageType('Sequence', (_message.Message,), {
  'DESCRIPTOR' : _SEQUENCE,
  '__module__' : 'mediapipe.modules.objectron.calculators.annotation_data_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.Sequence)
  })
_sym_db.RegisterMessage(Sequence)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NORMALIZEDPOINT2D._serialized_start=198
  _NORMALIZEDPOINT2D._serialized_end=254
  _POINT3D._serialized_start=256
  _POINT3D._serialized_end=298
  _ANNOTATEDKEYPOINT._serialized_start=301
  _ANNOTATEDKEYPOINT._serialized_end=434
  _OBJECTANNOTATION._serialized_start=437
  _OBJECTANNOTATION._serialized_end=597
  _FRAMEANNOTATION._serialized_start=600
  _FRAMEANNOTATION._serialized_end=785
  _SEQUENCE._serialized_start=787
  _SEQUENCE._serialized_end=888
# @@protoc_insertion_point(module_scope)
