import asyncio.locks
import enum
import modal._utils.blob_utils
import modal.client
import modal.object
import modal_proto.api_pb2
import pathlib
import synchronicity.combined_types
import typing
import typing_extensions

class FileEntryType(enum.IntEnum):
    """Type of a file entry listed from a Modal volume."""

    UNSPECIFIED = 0
    FILE = 1
    DIRECTORY = 2
    SYMLINK = 3

class FileEntry:
    path: str
    type: FileEntryType
    mtime: int
    size: int

    @classmethod
    def _from_proto(cls, proto: modal_proto.api_pb2.FileEntry) -> FileEntry: ...
    def __getattr__(self, name: str): ...
    def __init__(self, path: str, type: FileEntryType, mtime: int, size: int) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...
    def __setattr__(self, name, value): ...
    def __delattr__(self, name): ...
    def __hash__(self): ...

class _Volume(modal.object._Object):
    _lock: asyncio.locks.Lock

    def _initialize_from_empty(self): ...
    @staticmethod
    def new(): ...
    @staticmethod
    def from_name(
        label: str,
        namespace=1,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
        version: typing.Optional[int] = None,
    ) -> _Volume: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[_Volume],
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        version: typing.Optional[int] = None,
        _heartbeat_sleep: float = 300,
    ) -> typing.AsyncContextManager[_Volume]: ...
    @staticmethod
    def persisted(
        label: str, namespace=1, environment_name: typing.Optional[str] = None, cloud: typing.Optional[str] = None
    ): ...
    @staticmethod
    async def lookup(
        label: str,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
        version: typing.Optional[int] = None,
    ) -> _Volume: ...
    @staticmethod
    async def create_deployed(
        deployment_name: str,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        version: typing.Optional[int] = None,
    ) -> str: ...
    async def _do_reload(self, lock=True): ...
    async def commit(self): ...
    async def reload(self): ...
    def iterdir(self, path: str, *, recursive: bool = True) -> typing.AsyncIterator[FileEntry]: ...
    async def listdir(self, path: str, *, recursive: bool = False) -> typing.List[FileEntry]: ...
    def read_file(self, path: str) -> typing.AsyncIterator[bytes]: ...
    async def read_file_into_fileobj(self, path: str, fileobj: typing.IO[bytes]) -> int: ...
    async def remove_file(self, path: str, recursive: bool = False) -> None: ...
    async def copy_files(self, src_paths: typing.Sequence[str], dst_path: str) -> None: ...
    async def batch_upload(self, force: bool = False) -> _VolumeUploadContextManager: ...
    async def _instance_delete(self): ...
    @staticmethod
    async def delete(
        label: str, client: typing.Optional[modal.client._Client] = None, environment_name: typing.Optional[str] = None
    ): ...

class _VolumeUploadContextManager:
    _volume_id: str
    _client: modal.client._Client
    _force: bool
    progress_cb: typing.Callable[..., typing.Any]
    _upload_generators: typing.List[
        typing.Generator[typing.Callable[[], modal._utils.blob_utils.FileUploadSpec], None, None]
    ]

    def __init__(
        self,
        volume_id: str,
        client: modal.client._Client,
        progress_cb: typing.Optional[typing.Callable[..., typing.Any]] = None,
        force: bool = False,
    ): ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    def put_file(
        self,
        local_file: typing.Union[pathlib.Path, str, typing.BinaryIO],
        remote_path: typing.Union[pathlib.PurePosixPath, str],
        mode: typing.Optional[int] = None,
    ): ...
    def put_directory(
        self,
        local_path: typing.Union[pathlib.Path, str],
        remote_path: typing.Union[pathlib.PurePosixPath, str],
        recursive: bool = True,
    ): ...
    async def _upload_file(
        self, file_spec: modal._utils.blob_utils.FileUploadSpec
    ) -> modal_proto.api_pb2.MountFile: ...

class Volume(modal.object.Object):
    _lock: asyncio.locks.Lock

    def __init__(self, *args, **kwargs): ...
    def _initialize_from_empty(self): ...
    @staticmethod
    def new(): ...
    @staticmethod
    def from_name(
        label: str,
        namespace=1,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
        version: typing.Optional[int] = None,
    ) -> Volume: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[Volume],
        client: typing.Optional[modal.client.Client] = None,
        environment_name: typing.Optional[str] = None,
        version: typing.Optional[int] = None,
        _heartbeat_sleep: float = 300,
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Volume]: ...
    @staticmethod
    def persisted(
        label: str, namespace=1, environment_name: typing.Optional[str] = None, cloud: typing.Optional[str] = None
    ): ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
            version: typing.Optional[int] = None,
        ) -> Volume: ...
        async def aio(
            self,
            label: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
            version: typing.Optional[int] = None,
        ) -> Volume: ...

    lookup: __lookup_spec

    class __create_deployed_spec(typing_extensions.Protocol):
        def __call__(
            self,
            deployment_name: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            version: typing.Optional[int] = None,
        ) -> str: ...
        async def aio(
            self,
            deployment_name: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            version: typing.Optional[int] = None,
        ) -> str: ...

    create_deployed: __create_deployed_spec

    class ___do_reload_spec(typing_extensions.Protocol):
        def __call__(self, lock=True): ...
        async def aio(self, lock=True): ...

    _do_reload: ___do_reload_spec

    class __commit_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    commit: __commit_spec

    class __reload_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    reload: __reload_spec

    class __iterdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str, *, recursive: bool = True) -> typing.Iterator[FileEntry]: ...
        def aio(self, path: str, *, recursive: bool = True) -> typing.AsyncIterator[FileEntry]: ...

    iterdir: __iterdir_spec

    class __listdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str, *, recursive: bool = False) -> typing.List[FileEntry]: ...
        async def aio(self, path: str, *, recursive: bool = False) -> typing.List[FileEntry]: ...

    listdir: __listdir_spec

    class __read_file_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.Iterator[bytes]: ...
        def aio(self, path: str) -> typing.AsyncIterator[bytes]: ...

    read_file: __read_file_spec

    class __read_file_into_fileobj_spec(typing_extensions.Protocol):
        def __call__(self, path: str, fileobj: typing.IO[bytes]) -> int: ...
        async def aio(self, path: str, fileobj: typing.IO[bytes]) -> int: ...

    read_file_into_fileobj: __read_file_into_fileobj_spec

    class __remove_file_spec(typing_extensions.Protocol):
        def __call__(self, path: str, recursive: bool = False) -> None: ...
        async def aio(self, path: str, recursive: bool = False) -> None: ...

    remove_file: __remove_file_spec

    class __copy_files_spec(typing_extensions.Protocol):
        def __call__(self, src_paths: typing.Sequence[str], dst_path: str) -> None: ...
        async def aio(self, src_paths: typing.Sequence[str], dst_path: str) -> None: ...

    copy_files: __copy_files_spec

    class __batch_upload_spec(typing_extensions.Protocol):
        def __call__(self, force: bool = False) -> VolumeUploadContextManager: ...
        async def aio(self, force: bool = False) -> VolumeUploadContextManager: ...

    batch_upload: __batch_upload_spec

    class ___instance_delete_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    _instance_delete: ___instance_delete_spec

    class __delete_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ): ...
        async def aio(
            self,
            label: str,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ): ...

    delete: __delete_spec

class VolumeUploadContextManager:
    _volume_id: str
    _client: modal.client.Client
    _force: bool
    progress_cb: typing.Callable[..., typing.Any]
    _upload_generators: typing.List[
        typing.Generator[typing.Callable[[], modal._utils.blob_utils.FileUploadSpec], None, None]
    ]

    def __init__(
        self,
        volume_id: str,
        client: modal.client.Client,
        progress_cb: typing.Optional[typing.Callable[..., typing.Any]] = None,
        force: bool = False,
    ): ...
    def __enter__(self): ...
    async def __aenter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    def put_file(
        self,
        local_file: typing.Union[pathlib.Path, str, typing.BinaryIO],
        remote_path: typing.Union[pathlib.PurePosixPath, str],
        mode: typing.Optional[int] = None,
    ): ...
    def put_directory(
        self,
        local_path: typing.Union[pathlib.Path, str],
        remote_path: typing.Union[pathlib.PurePosixPath, str],
        recursive: bool = True,
    ): ...

    class ___upload_file_spec(typing_extensions.Protocol):
        def __call__(self, file_spec: modal._utils.blob_utils.FileUploadSpec) -> modal_proto.api_pb2.MountFile: ...
        async def aio(self, file_spec: modal._utils.blob_utils.FileUploadSpec) -> modal_proto.api_pb2.MountFile: ...

    _upload_file: ___upload_file_spec

def _open_files_error_annotation(mount_path: str) -> typing.Optional[str]: ...
