import base64
import sqlite3
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

import py_fast_rsync
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from loguru import logger

from syftbox.lib.lib import PermissionTree, SyftPermission, filter_metadata
from syftbox.server.settings import ServerSettings, get_server_settings
from syftbox.server.sync.db import (
    delete_file_metadata,
    get_all_datasites,
    get_all_metadata,
    get_db,
    get_one_metadata,
    move_with_transaction,
    save_file_metadata,
)
from syftbox.server.sync.hash import hash_file

from .models import (
    ApplyDiffRequest,
    ApplyDiffResponse,
    BatchFileRequest,
    DiffRequest,
    DiffResponse,
    FileMetadata,
    FileMetadataRequest,
    FileRequest,
)


def get_db_connection(request: Request):
    conn = get_db(request.state.server_settings.file_db_path)
    yield conn
    conn.close()


def get_file_metadata(
    req: FileMetadataRequest,
    conn=Depends(get_db_connection),
) -> list[FileMetadata]:
    # TODO check permissions

    try:
        return get_one_metadata(conn, path=req.path_like)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/get_diff", response_model=DiffResponse)
def get_diff(
    req: DiffRequest,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
) -> DiffResponse:
    try:
        metadata = get_one_metadata(conn, path=f"{req.path}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    abs_path = server_settings.snapshot_folder / metadata.path
    with open(abs_path, "rb") as f:
        data = f.read()

    diff = py_fast_rsync.diff(req.signature_bytes, data)
    diff_bytes = base64.b85encode(diff).decode("utf-8")
    return DiffResponse(
        path=metadata.path.as_posix(),
        diff=diff_bytes,
        hash=metadata.hash,
    )


@router.post("/datasite_states", response_model=dict[str, list[FileMetadata]])
def get_datasite_states(
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
    email: str = Header(),
) -> dict[str, list[FileMetadata]]:
    all_datasites = get_all_datasites(conn)
    datasite_states: dict[str, list[FileMetadata]] = {}
    for datasite in all_datasites:
        try:
            datasite_state = dir_state(Path(datasite), conn, server_settings, email)
        except Exception as e:
            logger.error(f"Failed to get dir state for {datasite}: {e}")
            continue
        datasite_states[datasite] = datasite_state

    return datasite_states


@router.post("/dir_state", response_model=list[FileMetadata])
def dir_state(
    dir: Path,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
    email: str = Header(),
) -> list[FileMetadata]:
    if dir.is_absolute():
        raise HTTPException(status_code=400, detail="dir must be relative")

    metadata = get_all_metadata(conn, path_like=f"{dir.as_posix()}")
    full_path = server_settings.snapshot_folder / dir
    # get the top level perm file
    try:
        perm_tree = PermissionTree.from_path(full_path, raise_on_corrupted_files=True)
    except Exception as e:
        logger.warning(f"Failed to parse permission tree: {dir}")
        raise e

    # filter the read state for this user by the perm tree
    filtered_metadata = filter_metadata(email, metadata, perm_tree, server_settings.snapshot_folder)
    return filtered_metadata


@router.post("/get_metadata", response_model=FileMetadata)
def get_metadata(
    metadata: FileMetadata = Depends(get_file_metadata),
) -> FileMetadata:
    return metadata


@router.post("/apply_diff", response_model=ApplyDiffResponse)
def apply_diffs(
    req: ApplyDiffRequest,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
) -> ApplyDiffResponse:
    try:
        metadata = get_one_metadata(conn, path=f"{req.path}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    abs_path = server_settings.snapshot_folder / metadata.path
    with open(abs_path, "rb") as f:
        data = f.read()
    result = py_fast_rsync.apply(data, req.diff_bytes)

    if SyftPermission.is_permission_file(metadata.path) and not SyftPermission.is_valid(result):
        raise HTTPException(status_code=400, detail="invalid syftpermission contents, skipped writing")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(result)
        temp_path = Path(temp_file.name)

    new_metadata = hash_file(temp_path)

    if new_metadata.hash != req.expected_hash:
        raise HTTPException(status_code=400, detail="expected_hash mismatch")

    # move temp path to real path and update db
    move_with_transaction(
        conn,
        metadata=new_metadata,
        origin_path=abs_path,
        server_settings=server_settings,
    )

    return ApplyDiffResponse(path=req.path, current_hash=new_metadata.hash, previous_hash=metadata.hash)


@router.post("/delete", response_class=JSONResponse)
def delete_file(
    req: FileRequest,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
) -> JSONResponse:
    try:
        metadata = get_one_metadata(conn, path=f"{req.path}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        delete_file_metadata(conn, metadata.path.as_posix())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    conn.commit()
    abs_path = server_settings.snapshot_folder / metadata.path
    Path(abs_path).unlink(missing_ok=True)
    return JSONResponse(content={"status": "success"})


@router.post("/create", response_class=JSONResponse)
def create_file(
    file: UploadFile,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
) -> JSONResponse:
    if "%" in file.filename:
        raise HTTPException(status_code=400, detail="filename cannot contain '%'")

    relative_path = Path(file.filename)
    abs_path = server_settings.snapshot_folder / relative_path

    contents = file.file.read()

    if SyftPermission.is_permission_file(relative_path) and not SyftPermission.is_valid(contents):
        raise HTTPException(status_code=400, detail="invalid syftpermission contents, skipped writing")

    abs_path.parent.mkdir(exist_ok=True, parents=True)

    with open(abs_path, "wb") as f:
        # better to use async aiosqlite
        f.write(contents)

    cursor = conn.cursor()
    try:
        get_one_metadata(cursor, path=f"{file.filename}")
        raise HTTPException(status_code=400, detail="file already exists")
    except ValueError:
        # this is ok, there should be no metadata in db
        pass

    # create a new metadata for db entry
    metadata = hash_file(abs_path, root_dir=server_settings.snapshot_folder)
    save_file_metadata(cursor, metadata)
    conn.commit()
    cursor.close()

    return JSONResponse(content={"status": "success"})


@router.post("/download", response_class=FileResponse)
def download_file(
    req: FileRequest,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
) -> FileResponse:
    try:
        metadata = get_one_metadata(conn, path=f"{req.path}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    abs_path = server_settings.snapshot_folder / metadata.path
    if not Path(abs_path).exists():
        # could be a stale db entry, remove from db
        delete_file_metadata(conn, metadata.path.as_posix())
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(abs_path)


@router.post("/datasites", response_model=list[str])
def get_datasites(conn: sqlite3.Connection = Depends(get_db_connection)) -> list[str]:
    return get_all_datasites(conn)


def create_zip_from_files(file_metadatas: list[FileMetadata], server_settings: ServerSettings) -> BytesIO:
    file_paths = [server_settings.snapshot_folder / file_metadata.path for file_metadata in file_metadatas]
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zf:
        for file_path in file_paths:
            with open(file_path, "rb") as file:
                zf.writestr(file_path.relative_to(server_settings.snapshot_folder).as_posix(), file.read())
    memory_file.seek(0)
    return memory_file


@router.post("/download_bulk")
async def get_files(
    req: BatchFileRequest,
    conn: sqlite3.Connection = Depends(get_db_connection),
    server_settings: ServerSettings = Depends(get_server_settings),
) -> StreamingResponse:
    all_metadata = []
    for path in req.paths:
        try:
            metadata = get_one_metadata(conn, path=path)
        except ValueError as e:
            logger.warning(str(e))
            continue

        abs_path = server_settings.snapshot_folder / metadata.path
        if not Path(abs_path).exists() or not Path(abs_path).is_file():
            logger.warning(f"File not found: {abs_path}")
            continue
        all_metadata.append(metadata)
    zip_file = create_zip_from_files(all_metadata, server_settings)
    return Response(content=zip_file.read(), media_type="application/zip")
