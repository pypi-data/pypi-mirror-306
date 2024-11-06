from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DELETED: ModelArtifactStatus
DESCRIPTOR: _descriptor.FileDescriptor
ERROR: ModelArtifactStatus
MODEL_TYPE_UNSPECIFIED: ModelType
PENDING_FILE: ModelArtifactStatus
PENDING_SCAN: ModelArtifactStatus
PYTHON: ModelType
PYTORCH: ModelType
READY: ModelArtifactStatus
STATUS_UNSPECIFIED: ModelArtifactStatus
TECTON_TEXT_EMBEDDING: ModelType

class CompleteModelArtifactUploadRequest(_message.Message):
    __slots__ = ["model_artifact_id", "part_etags", "upload_id"]
    class PartEtagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    PART_ETAGS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    model_artifact_id: _id__client_pb2.Id
    part_etags: _containers.ScalarMap[int, str]
    upload_id: str
    def __init__(self, model_artifact_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., upload_id: _Optional[str] = ..., part_etags: _Optional[_Mapping[int, str]] = ...) -> None: ...

class CompleteModelArtifactUploadResponse(_message.Message):
    __slots__ = ["key"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class CreateModelArtifactRequest(_message.Message):
    __slots__ = ["artifact_files", "description", "environments", "file_hashes", "input_schema", "model_config_file_path", "model_file_path", "name", "output_schema", "tags", "type"]
    class FileHashesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ARTIFACT_FILES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FILE_HASHES_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIG_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    MODEL_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    artifact_files: _containers.RepeatedScalarFieldContainer[str]
    description: str
    environments: _containers.RepeatedScalarFieldContainer[str]
    file_hashes: _containers.ScalarMap[str, str]
    input_schema: _schema__client_pb2.Schema
    model_config_file_path: str
    model_file_path: str
    name: str
    output_schema: _schema__client_pb2.Schema
    tags: _containers.ScalarMap[str, str]
    type: ModelType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[ModelType, str]] = ..., description: _Optional[str] = ..., file_hashes: _Optional[_Mapping[str, str]] = ..., input_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., output_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., model_file_path: _Optional[str] = ..., model_config_file_path: _Optional[str] = ..., artifact_files: _Optional[_Iterable[str]] = ..., environments: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateModelArtifactResponse(_message.Message):
    __slots__ = ["model_artifact_info"]
    MODEL_ARTIFACT_INFO_FIELD_NUMBER: _ClassVar[int]
    model_artifact_info: ModelArtifactInfo
    def __init__(self, model_artifact_info: _Optional[_Union[ModelArtifactInfo, _Mapping]] = ...) -> None: ...

class DeleteModelArtifactRequest(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    name: str
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class DeleteModelArtifactResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DescribeModelArtifactRequest(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    name: str
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class DescribeModelArtifactResponse(_message.Message):
    __slots__ = ["model_artifact_info"]
    MODEL_ARTIFACT_INFO_FIELD_NUMBER: _ClassVar[int]
    model_artifact_info: ModelArtifactInfo
    def __init__(self, model_artifact_info: _Optional[_Union[ModelArtifactInfo, _Mapping]] = ...) -> None: ...

class FetchModelArtifactRequest(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    name: str
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class FetchModelArtifactResponse(_message.Message):
    __slots__ = ["model_artifact_download_url", "model_config_download_url"]
    MODEL_ARTIFACT_DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIG_DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    model_artifact_download_url: str
    model_config_download_url: str
    def __init__(self, model_artifact_download_url: _Optional[str] = ..., model_config_download_url: _Optional[str] = ...) -> None: ...

class GetModelArtifactUploadUrlRequest(_message.Message):
    __slots__ = ["model_artifact_id"]
    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    model_artifact_id: _id__client_pb2.Id
    def __init__(self, model_artifact_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...

class GetModelArtifactUploadUrlResponse(_message.Message):
    __slots__ = ["model_artifact_id", "model_config_upload_url", "upload_id"]
    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIG_UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    model_artifact_id: _id__client_pb2.Id
    model_config_upload_url: str
    upload_id: str
    def __init__(self, model_artifact_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., upload_id: _Optional[str] = ..., model_config_upload_url: _Optional[str] = ...) -> None: ...

class GetTectonModelInfoRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetTectonModelInfoResponse(_message.Message):
    __slots__ = ["model_info"]
    MODEL_INFO_FIELD_NUMBER: _ClassVar[int]
    model_info: ModelInfo
    def __init__(self, model_info: _Optional[_Union[ModelInfo, _Mapping]] = ...) -> None: ...

class ListModelArtifactsRequest(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    name: str
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class ListModelArtifactsResponse(_message.Message):
    __slots__ = ["models"]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[ModelArtifactInfo]
    def __init__(self, models: _Optional[_Iterable[_Union[ModelArtifactInfo, _Mapping]]] = ...) -> None: ...

class ListTectonModelsRequest(_message.Message):
    __slots__ = ["filter"]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: str
    def __init__(self, filter: _Optional[str] = ...) -> None: ...

class ListTectonModelsResponse(_message.Message):
    __slots__ = ["models"]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[ModelInfo]
    def __init__(self, models: _Optional[_Iterable[_Union[ModelInfo, _Mapping]]] = ...) -> None: ...

class ModelArtifactInfo(_message.Message):
    __slots__ = ["artifact_files", "created_at", "created_by", "created_by_principal", "description", "environments", "file_hashes", "id", "input_schema", "model_config_file_path", "model_file_path", "name", "output_schema", "status", "storage_path", "tags", "type", "updated_at"]
    class FileHashesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ARTIFACT_FILES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FILE_HASHES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIG_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    MODEL_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    artifact_files: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.Principal
    created_by_principal: _principal__client_pb2.PrincipalBasic
    description: str
    environments: _containers.RepeatedScalarFieldContainer[str]
    file_hashes: _containers.ScalarMap[str, str]
    id: _id__client_pb2.Id
    input_schema: _schema__client_pb2.Schema
    model_config_file_path: str
    model_file_path: str
    name: str
    output_schema: _schema__client_pb2.Schema
    status: ModelArtifactStatus
    storage_path: str
    tags: _containers.ScalarMap[str, str]
    type: ModelType
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ..., type: _Optional[_Union[ModelType, str]] = ..., description: _Optional[str] = ..., file_hashes: _Optional[_Mapping[str, str]] = ..., input_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., output_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., storage_path: _Optional[str] = ..., status: _Optional[_Union[ModelArtifactStatus, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., model_file_path: _Optional[str] = ..., model_config_file_path: _Optional[str] = ..., artifact_files: _Optional[_Iterable[str]] = ..., environments: _Optional[_Iterable[str]] = ..., created_by: _Optional[_Union[_principal__client_pb2.Principal, _Mapping]] = ..., created_by_principal: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ...) -> None: ...

class ModelInfo(_message.Message):
    __slots__ = ["id", "metadata_public_uri", "model_public_uri", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_PUBLIC_URI_FIELD_NUMBER: _ClassVar[int]
    MODEL_PUBLIC_URI_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _id__client_pb2.Id
    metadata_public_uri: str
    model_public_uri: str
    name: str
    def __init__(self, id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ..., model_public_uri: _Optional[str] = ..., metadata_public_uri: _Optional[str] = ...) -> None: ...

class UpdateTectonModelRequest(_message.Message):
    __slots__ = ["artifact_files", "description", "environments", "id", "input_schema", "model_config_file_path", "model_file_path", "name", "output_schema", "tags", "type"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ARTIFACT_FILES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    MODEL_CONFIG_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    MODEL_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    artifact_files: _containers.RepeatedScalarFieldContainer[str]
    description: str
    environments: _containers.RepeatedScalarFieldContainer[str]
    id: _id__client_pb2.Id
    input_schema: _schema__client_pb2.Schema
    model_config_file_path: str
    model_file_path: str
    name: str
    output_schema: _schema__client_pb2.Schema
    tags: _containers.ScalarMap[str, str]
    type: ModelType
    def __init__(self, name: _Optional[str] = ..., id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., type: _Optional[_Union[ModelType, str]] = ..., description: _Optional[str] = ..., input_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., output_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., model_file_path: _Optional[str] = ..., model_config_file_path: _Optional[str] = ..., artifact_files: _Optional[_Iterable[str]] = ..., environments: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateTectonModelResponse(_message.Message):
    __slots__ = ["model_config_upload_url"]
    MODEL_CONFIG_UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    model_config_upload_url: str
    def __init__(self, model_config_upload_url: _Optional[str] = ...) -> None: ...

class UploadModelArtifactPartRequest(_message.Message):
    __slots__ = ["model_artifact_id", "parent_upload_id", "part_number"]
    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    model_artifact_id: _id__client_pb2.Id
    parent_upload_id: str
    part_number: int
    def __init__(self, model_artifact_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., parent_upload_id: _Optional[str] = ..., part_number: _Optional[int] = ...) -> None: ...

class UploadModelArtifactPartResponse(_message.Message):
    __slots__ = ["upload_url"]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    upload_url: str
    def __init__(self, upload_url: _Optional[str] = ...) -> None: ...

class ModelArtifactStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
