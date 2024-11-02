from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActivateDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class ActivateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IndexDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class IndexDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeployKubeComponentsRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class DeployKubeComponentsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RebuildDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "new_image_tag", "base_image_override", "enable_profiling")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_IMAGE_TAG_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    new_image_tag: str
    base_image_override: str
    enable_profiling: bool
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        new_image_tag: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        enable_profiling: bool = ...,
    ) -> None: ...

class RebuildDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class RedeployDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "enable_profiling")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    enable_profiling: bool
    def __init__(self, existing_deployment_id: _Optional[str] = ..., enable_profiling: bool = ...) -> None: ...

class RedeployDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class UploadSourceRequest(_message.Message):
    __slots__ = (
        "deployment_id",
        "archive",
        "no_promote",
        "dependency_hash",
        "base_image_override",
        "use_grpc",
        "enable_profiling",
    )
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    NO_PROMOTE_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    USE_GRPC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    archive: bytes
    no_promote: bool
    dependency_hash: str
    base_image_override: str
    use_grpc: bool
    enable_profiling: bool
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        archive: _Optional[bytes] = ...,
        no_promote: bool = ...,
        dependency_hash: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        use_grpc: bool = ...,
        enable_profiling: bool = ...,
    ) -> None: ...

class UploadSourceResponse(_message.Message):
    __slots__ = ("status", "progress_url")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_URL_FIELD_NUMBER: _ClassVar[int]
    status: str
    progress_url: str
    def __init__(self, status: _Optional[str] = ..., progress_url: _Optional[str] = ...) -> None: ...
