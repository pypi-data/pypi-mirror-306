from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserDefinedFunction(_message.Message):
    __slots__ = ["body", "name"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    body: str
    name: str
    def __init__(self, name: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...
