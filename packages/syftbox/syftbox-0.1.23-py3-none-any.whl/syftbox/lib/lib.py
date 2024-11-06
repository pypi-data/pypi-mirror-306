from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
import tempfile
import threading
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock

import httpx
import requests
from loguru import logger
from typing_extensions import Any, Optional, Self, Tuple, Union

from syftbox.server.sync.models import FileMetadata

from .exceptions import ClientConfigException

current_dir = Path(__file__).parent
ASSETS_FOLDER = current_dir.parent / "assets"
DEFAULT_PORT = 8082
ICON_FOLDER = ASSETS_FOLDER / "icon"
DEFAULT_SERVER_URL = "https://syftbox.openmined.org"
DEFAULT_SYNC_FOLDER = Path("~/SyftBox").expanduser().resolve()
DEFAULT_CONFIG_FOLDER = Path("~/.syftbox").expanduser().resolve()
DEFAULT_CONFIG_PATH = Path(DEFAULT_CONFIG_FOLDER, "client_config.json")
DEFAULT_LOGS_PATH = Path(DEFAULT_CONFIG_FOLDER, "logs", "syftbox.log")

USER_GROUP_GLOBAL = "GLOBAL"
DIR_NOT_EMPTY = "Directory is not empty"

ICON_FILE = "Icon"  # special
IGNORE_FILES = []


def perm_file_path(path: str) -> str:
    return f"{path}/_.syftperm"


def is_primitive_json_serializable(obj):
    if isinstance(obj, (str, int, float, bool, type(None))):
        return True
    return False


def pack(obj) -> Any:
    if is_primitive_json_serializable(obj):
        return obj

    if hasattr(obj, "to_dict"):
        return obj.to_dict()

    if isinstance(obj, list):
        return [pack(val) for val in obj]

    if isinstance(obj, dict):
        return {k: pack(v) for k, v in obj.items()}

    if isinstance(obj, Path):
        return str(obj)

    raise Exception(f"Unable to pack type: {type(obj)} value: {obj}")


class Jsonable:
    def to_dict(self) -> dict:
        output = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            output[k] = pack(v)
        return output

    def __iter__(self):
        for key, val in self.to_dict().items():
            if key.startswith("_"):
                yield key, val

    def __getitem__(self, key):
        if key.startswith("_"):
            return None
        return self.to_dict()[key]

    @classmethod
    def load(cls, file_or_bytes: Union[str, Path, bytes]) -> Self:
        try:
            if isinstance(file_or_bytes, (str, Path)):
                with open(file_or_bytes) as f:
                    data = f.read()
            else:
                data = file_or_bytes
            d = json.loads(data)
            return cls(**d)
        except Exception as e:
            raise e

    def save(self, filepath: str) -> None:
        d = self.to_dict()
        with open(Path(filepath).expanduser(), "w") as f:
            f.write(json.dumps(d))


@dataclass
class SyftPermission(Jsonable):
    admin: list[str]
    read: list[str]
    write: list[str]
    filepath: Optional[str] = None
    terminal: bool = False

    @classmethod
    def datasite_default(cls, email: str) -> Self:
        return cls(
            admin=[email],
            read=[email],
            write=[email],
        )

    @staticmethod
    def is_permission_file(path: Union[Path, str], check_exists: bool = False) -> bool:
        path = Path(path)
        if check_exists and not path.is_file():
            return False
        return path.name == "_.syftperm"

    @classmethod
    def is_valid(cls, path_or_bytes: Union[str, Path, bytes]):
        try:
            SyftPermission.load(path_or_bytes)
            return True
        except Exception:
            return False

    def is_admin(self, email: str) -> bool:
        return email in self.admin

    def has_read_permission(self, email: str) -> bool:
        return email in self.read or USER_GROUP_GLOBAL in self.read

    def has_write_permission(self, email: str) -> bool:
        return email in self.write or USER_GROUP_GLOBAL in self.write

    def __eq__(self, other):
        if not isinstance(other, SyftPermission):
            return NotImplemented
        return (
            self.admin == other.admin
            and self.read == other.read
            and self.write == other.write
            and self.filepath == other.filepath
            and self.terminal == other.terminal
        )

    def perm_path(self, path=None) -> str:
        if path is not None:
            self.filepath = path

        if self.filepath is None:
            raise Exception(f"Saving requites a path: {self}")

        if os.path.isdir(self.filepath):
            self.filepath = perm_file_path(self.filepath)
        return self.filepath

    def save(self, path=None) -> bool:
        self.perm_path(path=path)
        if self.filepath.endswith(".syftperm"):
            super().save(self.filepath)
        else:
            raise Exception(f"Perm file must end in .syftperm. {self.filepath}")
        return True

    def ensure(self, path=None) -> bool:
        # make sure the contents matches otherwise write it
        self.perm_path(path=path)
        try:
            prev_perm_file = SyftPermission.load(self.filepath)
            if self == prev_perm_file:
                # no need to write
                return True
        except Exception:
            pass
        return self.save(path)

    @classmethod
    def no_permission(cls) -> Self:
        return cls(admin=[], read=[], write=[])

    @classmethod
    def mine_no_permission(cls, email: str) -> Self:
        return cls(admin=[email], read=[], write=[])

    @classmethod
    def mine_with_public_read(cls, email: str) -> Self:
        return cls(admin=[email], read=[email, "GLOBAL"], write=[email])

    @classmethod
    def mine_with_public_write(cls, email: str) -> Self:
        return cls(admin=[email], read=[email, "GLOBAL"], write=[email, "GLOBAL"])

    @classmethod
    def theirs_with_my_read(cls, their_email, my_email: str) -> Self:
        return cls(admin=[their_email], read=[their_email, my_email], write=[their_email])

    @classmethod
    def theirs_with_my_read_write(cls, their_email, my_email: str) -> Self:
        return cls(
            admin=[their_email],
            read=[their_email, my_email],
            write=[their_email, my_email],
        )

    def __repr__(self) -> str:
        string = "SyftPermission:\n"
        string += f"{self.filepath}\n"
        string += "ADMIN: ["
        for v in self.admin:
            string += v + ", "
        string += "]\n"

        string += "READ: ["
        for r in self.read:
            string += r + ", "
        string += "]\n"

        string += "WRITE: ["
        for w in self.write:
            string += w + ", "
        string += "]\n"
        return string


def bintostr(binary_data):
    return base64.b85encode(zlib.compress(binary_data)).decode("utf-8")


def strtobin(encoded_data):
    return zlib.decompress(base64.b85decode(encoded_data.encode("utf-8")))


def get_symlink(file_path) -> str:
    return os.readlink(file_path)


def is_symlink(file_path) -> bool:
    return os.path.islink(file_path)


# def symlink_to_syftlink(file_path):
#     return SyftLink.from_path(file_path)


# def convert_to_symlink(path):
#     if not is_symlink(path):
#         raise Exception(f"Cant convert a non symlink {path}")
#     abs_path = get_symlink(path)
#     syft_link = symlink_to_syftlink(abs_path)
#     return str(syft_link)


def ignore_dirs(directory: str, root: str, ignore_folders=None) -> bool:
    if ignore_folders is not None:
        for ignore_folder in ignore_folders:
            if root.endswith(ignore_folder):
                return True
    return False


def ignore_file(directory: str, root: str, filename: str) -> bool:
    if directory == root:
        if filename.startswith(ICON_FILE):
            return True
        if filename in IGNORE_FILES:
            return True
    if filename == ".DS_Store":
        return True
    return False


def get_datasites(sync_folder: Union[str, Path]) -> list[str]:
    sync_folder = str(sync_folder.resolve()) if isinstance(sync_folder, Path) else sync_folder
    datasites = []
    folders = os.listdir(sync_folder)
    for folder in folders:
        if "@" in folder:
            datasites.append(folder)
    return datasites


def build_tree_string(paths_dict, prefix=""):
    lines = []
    items = list(paths_dict.items())

    for index, (key, value) in enumerate(items):
        # Determine if it's the last item in the current directory level
        connector = "└── " if index == len(items) - 1 else "├── "
        lines.append(f"{prefix}{connector}{repr(key)}")

        # Prepare the prefix for the next level
        if isinstance(value, dict):
            extension = "    " if index == len(items) - 1 else "│   "
            lines.append(build_tree_string(value, prefix + extension))

    return "\n".join(lines)


@dataclass
class PermissionTree(Jsonable):
    tree: dict[str, SyftPermission]
    parent_path: str
    root_perm: Optional[SyftPermission]

    corrupted_permission_files: list[str] = field(default_factory=list)

    @classmethod
    def from_path(cls, parent_path, raise_on_corrupted_files: bool = False) -> Self:
        corrupted_permission_files = []
        perm_dict = {}
        for root, dirs, files in os.walk(parent_path):
            for file in files:
                if file.endswith(".syftperm"):
                    path = os.path.join(root, file)
                    try:
                        perm_dict[path] = SyftPermission.load(path)
                    except Exception:
                        corrupted_permission_files.append(path)

        root_perm = None
        root_perm_path = perm_file_path(parent_path)
        if root_perm_path in perm_dict:
            root_perm = perm_dict[root_perm_path]

        if corrupted_permission_files:
            if raise_on_corrupted_files:
                raise ValueError(f"Found corrupted permission files: {corrupted_permission_files}")
            logger.warning(f"Found corrupted permission files: {corrupted_permission_files}")

        return cls(
            root_perm=root_perm,
            tree=perm_dict,
            parent_path=parent_path,
            corrupted_permission_files=corrupted_permission_files,
        )

    def has_corrupted_permission(self, path: Union[str, Path]) -> bool:
        path = Path(path).resolve()
        corrupted_permission_paths = [Path(p).parent.resolve() for p in self.corrupted_permission_files]
        for perm_path in corrupted_permission_paths:
            if path.is_relative_to(perm_path):
                return True
        return False

    @property
    def root_or_default(self) -> SyftPermission:
        if self.root_perm:
            return self.root_perm
        return SyftPermission.no_permission()

    def permission_for_path(self, path: str) -> SyftPermission:
        parent_path = os.path.normpath(self.parent_path)
        current_perm = self.root_or_default

        # default
        if parent_path not in path:
            return current_perm

        sub_path = path.replace(parent_path, "")
        current_perm_level = parent_path
        for part in sub_path.split("/"):
            if part == "":
                continue

            current_perm_level += "/" + part
            next_perm_file = perm_file_path(current_perm_level)
            if next_perm_file in self.tree:
                next_perm = self.tree[next_perm_file]
                current_perm = next_perm

            if current_perm.terminal:
                return current_perm

        return current_perm

    def __repr__(self) -> str:
        return f"PermissionTree: {self.parent_path}\n" + build_tree_string(self.tree)


def filter_metadata(
    user_email: str,
    metadata_list: list[FileMetadata],
    perm_tree: PermissionTree,
    snapshot_folder: Path,
) -> list[FileMetadata]:
    filtered_metadata = []
    for metadata in metadata_list:
        perm_file_at_path = perm_tree.permission_for_path((snapshot_folder / metadata.path).as_posix())
        if (
            user_email in perm_file_at_path.read
            or "GLOBAL" in perm_file_at_path.read
            or user_email in perm_file_at_path.admin
        ):
            filtered_metadata.append(metadata)
    return filtered_metadata


class ResettableTimer:
    def __init__(self, timeout, callback, *args, **kwargs):
        self.timeout = timeout
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.timer = None
        self.lock = threading.Lock()

    def _run_callback(self):
        with self.lock:
            self.timer = None
        self.callback(*self.args, **self.kwargs)

    def start(self, *args, **kwargs):
        with self.lock:
            if self.timer:
                self.timer.cancel()

            # If new arguments are passed in start, they will overwrite the initial ones
            if args or kwargs:
                self.args = args
                self.kwargs = kwargs

            self.timer = threading.Timer(self.timeout, self._run_callback)
            self.timer.start()

    def cancel(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None


class SharedState:
    def __init__(self, client_config: ClientConfig):
        self.data = {}
        self.lock = Lock()
        self.client_config = client_config
        self.timers: dict[str:ResettableTimer] = {}
        self.fs_events = []

    @property
    def sync_folder(self) -> str:
        return self.client_config.sync_folder

    def get(self, key, default=None):
        with self.lock:
            if key == "my_datasites":
                return self._get_datasites()
            return self.data.get(key, default)

    def set(self, key, value):
        with self.lock:
            self.data[key] = value

    def _get_datasites(self):
        syft_folder = self.data.get(self.client_config.sync_folder)
        if not syft_folder or not os.path.exists(syft_folder):
            return []

        return [folder for folder in os.listdir(syft_folder) if os.path.isdir(os.path.join(syft_folder, folder))]


def get_root_data_path() -> Path:
    # get the PySyft / data directory to share datasets between notebooks
    # on Linux and MacOS the directory is: ~/.syft/data"
    # on Windows the directory is: C:/Users/$USER/.syft/data

    data_dir = Path.home() / ".syft" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir


def autocache(url: str, extension: Optional[str] = None, cache: bool = True) -> Optional[Path]:
    try:
        data_path = get_root_data_path()
        file_hash = hashlib.sha256(url.encode("utf8")).hexdigest()
        filename = file_hash
        if extension:
            filename += f".{extension}"
        file_path = data_path / filename
        if os.path.exists(file_path) and cache:
            return file_path
        return download_file(url, file_path)
    except Exception as e:
        logger.info(f"Failed to autocache: {url}. {e}")
        return None


def download_file(url: str, full_path: Union[str, Path]) -> Optional[Path]:
    full_path = Path(full_path)
    if not full_path.exists():
        r = requests.get(url, allow_redirects=True, verify=verify_tls())  # nosec
        if not r.ok:
            logger.info(f"Got {r.status_code} trying to download {url}")
            return None
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(r.content)
    return full_path


def verify_tls() -> bool:
    return not str_to_bool(str(os.environ.get("IGNORE_TLS_ERRORS", "0")))


def str_to_bool(bool_str: Optional[str]) -> bool:
    result = False
    bool_str = str(bool_str).lower()
    if bool_str == "true" or bool_str == "1":
        result = True
    return result


@dataclass
class Client(Jsonable):
    config_path: Path
    sync_folder: Path
    email: str
    port: int = DEFAULT_PORT
    server_url: str = "http://localhost:5001"
    token: Optional[int] = None
    email_token: Optional[str] = None
    autorun_plugins: Optional[list[str]] = field(default_factory=lambda: ["init", "create_datasite", "sync", "apps"])
    _server_client: Optional[httpx.Client] = None

    @property
    def is_registered(self) -> bool:
        return self.token is not None

    @property
    def server_client(self) -> httpx.Client:
        if self._server_client is None:
            self._server_client = httpx.Client(
                base_url=self.server_url,
                follow_redirects=True,
            )
        return self._server_client

    def close(self):
        if self._server_client:
            self._server_client.close()

    def save(self, path: Optional[int] = None) -> None:
        if path is None:
            path = self.config_path
        super().save(path)

    @property
    def datasite_path(self) -> Path:
        return Path(self.sync_folder) / self.email

    @property
    def manifest_path(self) -> Path:
        return os.path.join(self.datasite_path, "public/manifest/manifest.json")

    def get_datasites(self: str) -> list[str]:
        datasites = []
        folders = os.listdir(self.sync_folder)
        for folder in folders:
            if "@" in folder:
                datasites.append(folder)
        return datasites

    def use(self):
        os.environ["SYFTBOX_CURRENT_CLIENT"] = self.config_path
        os.environ["SYFTBOX_SYNC_DIR"] = self.sync_folder
        logger.info(f"> Setting Sync Dir to: {self.sync_folder}")

    def create_folder(self, path: str, permission: SyftPermission):
        os.makedirs(path, exist_ok=True)
        permission.save(path)

    @property
    def root_dir(self) -> Path:
        root_dir = Path(os.path.abspath(os.path.dirname(self.file_path) + "/../"))
        return root_dir

    def create_public_folder(self, path: str):
        full_path = self.root_dir / path
        os.makedirs(str(full_path), exist_ok=True)
        public_read = SyftPermission.mine_with_public_read(email=self.datasite)
        public_read.save(full_path)
        return Path(full_path)

    @classmethod
    def load(cls, filepath: Optional[Path] = None) -> Self:
        try:
            if filepath is None:
                config_path = os.getenv("SYFTBOX_CLIENT_CONFIG_PATH", DEFAULT_CONFIG_PATH)
                filepath = config_path
            return super().load(filepath)
        except Exception as e:
            raise ClientConfigException(
                f"Unable to load Client config from {filepath}."
                "If you are running this outside of syftbox app runner you must supply "
                "the Client config path like so: \n"
                "SYFTBOX_CLIENT_CONFIG_PATH=~/.syftbox/client_config.json"
            ) from e


ClientConfig = Client


def is_valid_dir(path: Union[str, Path], check_empty=True, check_writable=True) -> Tuple[bool, str]:
    try:
        if not path:
            return False, "Empty path"

        # Convert to Path object if string
        dir_path = Path(path).expanduser().resolve()

        # Must not be a reserved path
        if dir_path.is_reserved():
            return False, "Reserved path"

        if dir_path.exists():
            if not dir_path.is_dir():
                return False, "Path is not a directory"

            if check_empty and any(dir_path.iterdir()):
                return False, DIR_NOT_EMPTY
        elif check_writable:
            # Try to create a temporary file to test write permissions on parent
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                testfile = tempfile.TemporaryFile(dir=dir_path)
                testfile.close()
                shutil.rmtree(dir_path)
            except Exception as e:
                return False, str(e)

        # all checks passed
        return True, ""
    except Exception as e:
        return False, str(e)


def is_valid_email(email: str) -> bool:
    # Define a regex pattern for a valid email
    # from: https://stackoverflow.com/a/21608610
    email_regex = r"\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"

    # Use the match method to check if the email fits the pattern
    if re.match(email_regex, email):
        return True
    return False
