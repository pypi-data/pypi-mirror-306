import os
from typing import Iterator

import requests
from rich.progress import Progress

DEFAULT_CHUNK_SIZE = 1 << 12


class ChunkedFileReader:
    def __init__(self, file_name: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> None:
        self._file_name = file_name
        self._chunk_size = chunk_size
        self._total_size = os.path.getsize(file_name)
        self._chunks = self.chunks()

    def chunks(self) -> Iterator[bytes]:
        with open(self._file_name, "rb") as file, Progress() as progress:
            upload_task = progress.add_task(f"Uploading {self._file_name}", total=self._total_size)
            while True:
                data = file.read(self._chunk_size)
                if not data:
                    break
                progress.update(upload_task, advance=len(data))
                yield data

    def read(self, block_size: int = -1) -> bytes:  # block_size is ignored since we have predefined chunk_size
        return next(self._chunks, b"")

    def __len__(self) -> int:
        return self._total_size


def upload_file_to_s3(file_path: str, presigned_url: str) -> requests.Response:
    """
    Uploads a file to an S3 bucket using a pre-signed URL.

    :param file_path: Path to the file to upload
    :param presigned_url: Pre-signed URL to upload the file
    """
    response = requests.put(presigned_url, data=ChunkedFileReader(file_path))
    return response
