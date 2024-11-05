# pylint: disable=protected-access
# Copyright (c) Shipt, Inc.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import io
import tempfile
import zipfile as zp
from pathlib import Path
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from starlette.requests import ClientDisconnect
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.parser import parse_content_boundary
from streaming_form_data.validators import MaxSizeValidator

from opsml.app.core.dependencies import (
    reverse_swap_opsml_root,
    swap_opsml_root,
    verify_token,
)
from opsml.app.routes.pydantic_models import (
    DeleteFileResponse,
    FileExistsResponse,
    ListFileResponse,
)
from opsml.app.routes.utils import (
    ExternalFileTarget,
    MaxBodySizeException,
    MaxBodySizeValidator,
)
from opsml.helpers.logging import ArtifactLogger
from opsml.settings.config import config
from opsml.storage.client import get_storage_client

logger = ArtifactLogger.get_logger()


MAX_FILE_SIZE = 1024 * 1024 * 1024 * 50  # = 50GB
MAX_REQUEST_BODY_SIZE = MAX_FILE_SIZE + 1024
router = APIRouter()


def write_log(message: str) -> None:
    logger.info(message)


@router.post("/files/upload", name="upload", dependencies=[Depends(verify_token)])
async def upload_file(request: Request) -> Dict[str, str]:  # pragma: no cover
    """Uploads files in chunks to storage destination"""
    write_path = request.headers.get("write_path")

    boundary = parse_content_boundary(request.headers)
    logger.info(f"Boundary: {boundary}")

    if write_path is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No write path provided",
        )

    _write_path = Path(swap_opsml_root(request, Path(write_path)))
    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    try:
        target = ExternalFileTarget(
            write_path=_write_path,
            storage_client=get_storage_client(request.app.state.config),
            validator=MaxSizeValidator(MAX_FILE_SIZE),
        )

        parser = StreamingFormDataParser(headers=request.headers)
        parser.register("file", target)

        logger.info("headers {}", request.headers)
        async for chunk in request.stream():
            body_validator.check(chunk)
            parser.data_received(chunk)

    except ClientDisconnect:
        logger.error("Client disconnected")

    except MaxBodySizeException as error:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"""
              Maximum request body size limit ({MAX_REQUEST_BODY_SIZE}.
              Bytes exceeded ({error.body_len} bytes read)""",
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error uploading the file. {error}",
        ) from error

    return {"storage_uri": _write_path.as_posix()}


@router.get("/files/download", name="download_file")
def download_file(
    request: Request,
    path: str,
    background_tasks: BackgroundTasks,
) -> StreamingResponse:
    """Downloads a file

    Args:
        request:
            request object
        path:
            path to file

    Returns:
        Streaming file response
    """
    logger.info("Server: Downloading file {}", path)
    try:
        storage_client = get_storage_client(request.app.state.config)
        file_path = Path(swap_opsml_root(request, Path(path)))
        background_tasks.add_task(write_log, f"Downloaded file {file_path}")
        return StreamingResponse(
            storage_client.iterfile(file_path, config.download_chunk_size), media_type="application/octet-stream"
        )

    except Exception as error:
        logger.error("Server: Error downloading file {}", path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error downloading the file. {error}",
        ) from error


def download_dir(request: Request, path: Path) -> StreamingResponse:
    """Downloads a directory as a zip file

    Args:
        request:
            request object
        path:
            str

    Returns:
        Streaming file response
    """
    path = swap_opsml_root(request, path)
    try:
        storage_client = get_storage_client(request.app.state.config)
        logger.info("Server: Creating zip file for {}", path)
        zip_io = io.BytesIO()

        with tempfile.TemporaryDirectory() as tmpdirname:
            with zp.ZipFile(zip_io, mode="w", compression=zp.ZIP_DEFLATED) as temp_zip:
                lpath = Path(tmpdirname)
                zipfile = lpath / "artifacts"
                rpath = Path(path)
                files = storage_client.find(rpath)

                for file_ in files:
                    curr_rpath = Path(file_)
                    curr_lpath = lpath / curr_rpath.relative_to(rpath)
                    logger.info("Server: Downloading {} to {}", curr_rpath, curr_lpath)
                    storage_client.get(curr_rpath, curr_lpath)
                    zip_filepath = zipfile / curr_rpath.relative_to(rpath)
                    temp_zip.write(curr_lpath, zip_filepath)

            logger.info("Server: Sending zip file for {}", path)
            zip_io.seek(0)

            return StreamingResponse(
                storage_client.iterbuffer(zip_io, config.download_chunk_size),
                media_type="application/x-zip-compressed",
            )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error downloading the file. {error}",
        ) from error


@router.get("/files/download/ui", name="download_artifacts")
def download_artifacts_ui(request: Request, path: str) -> StreamingResponse:
    """Downloads a file

    Args:
        request:
            request object
        path:
            path to file

    Returns:
        Streaming file response
    """
    if Path(path).suffix == "":
        return download_dir(request, Path(path))

    background_tasks = BackgroundTasks()
    return download_file(request, path, background_tasks)


@router.get("/files/list", name="list_files")
def list_files(request: Request, path: str) -> ListFileResponse:
    """Lists files

    Args:
        request:
            request object
        path:
            path to read

    Returns:
        `ListFileResponse`
    """

    swapped_path = swap_opsml_root(request, Path(path))
    try:
        storage_client = get_storage_client(request.app.state.config)
        files = storage_client.find(Path(swapped_path))
        return ListFileResponse(files=[str(reverse_swap_opsml_root(request, Path(file_))) for file_ in files])

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error listing files. {error}",
        ) from error


@router.get("/files/exists", name="file_exists")
def file_exists(request: Request, path: str) -> FileExistsResponse:
    """Checks if path exists

    Args:
        request:
            request object
        path:
            path to files

    Returns:
        FileExistsResponse
    """
    storage_client = get_storage_client(request.app.state.config)
    return FileExistsResponse(
        exists=storage_client.exists(
            Path(
                swap_opsml_root(request, Path(path)),
            )
        ),
    )


@router.get("/files/delete", name="delete_files", dependencies=[Depends(verify_token)])
def delete_files(request: Request, path: str) -> DeleteFileResponse:
    """Deletes a file

    Args:
        request:
            request object
        path:
            path to file

    Returns:
        `DeleteFileResponse`
    """

    try:
        try:
            storage_client = get_storage_client(request.app.state.config)
            storage_client.rm(Path(swap_opsml_root(request, Path(path))))
            return DeleteFileResponse(deleted=True)

        except FileNotFoundError:
            logger.warning(f"File {path} not found. It may have already been deleted")
            return DeleteFileResponse(deleted=True)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error deleting files. {error}",
        ) from error
