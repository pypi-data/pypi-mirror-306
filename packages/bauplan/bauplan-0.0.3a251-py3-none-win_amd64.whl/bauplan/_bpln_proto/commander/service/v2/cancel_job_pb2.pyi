from bauplan._bpln_proto.commander.service.v2 import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CancelJobRequest(_message.Message):
    __slots__ = ('job_id',)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: _common_pb2.JobId
    def __init__(self, job_id: _Optional[_Union[_common_pb2.JobId, _Mapping]] = ...) -> None: ...

class CancelJobResponse(_message.Message):
    __slots__ = ('status', 'message')
    class CancelStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CancelJobResponse.CancelStatus]
        FAILURE: _ClassVar[CancelJobResponse.CancelStatus]

    SUCCESS: CancelJobResponse.CancelStatus
    FAILURE: CancelJobResponse.CancelStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: CancelJobResponse.CancelStatus
    message: str
    def __init__(
        self,
        status: _Optional[_Union[CancelJobResponse.CancelStatus, str]] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...
