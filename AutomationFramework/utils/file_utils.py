from __future__ import annotations

import threading
from pathlib import Path


class FileDownloadVerifier:
    @staticmethod
    def wait_for_download(download_dir: str | Path, expected_name: str | None = None, timeout: int = 30) -> Path:
        directory = Path(download_dir)
        if not directory.exists():
            raise FileNotFoundError(f"Download directory not found: {directory}")

        deadline = timeout
        stable_sizes: dict[Path, int] = {}
        start_seconds = 0.0

        import time

        start_seconds = time.monotonic()
        while time.monotonic() - start_seconds < deadline:
            for file_path in directory.iterdir():
                if not file_path.is_file():
                    continue
                if expected_name and expected_name not in file_path.name:
                    continue
                if file_path.suffix in {".crdownload", ".tmp"}:
                    continue

                current_size = file_path.stat().st_size
                previous_size = stable_sizes.get(file_path)
                if current_size > 0 and previous_size == current_size:
                    return file_path
                stable_sizes[file_path] = current_size

            threading.Event().wait(0.5)

        raise TimeoutError(f"File download did not complete within {timeout} seconds in {directory}")

    @staticmethod
    def latest_file(download_dir: str | Path, extension: str | None = None) -> Path:
        directory = Path(download_dir)
        files = [file_path for file_path in directory.iterdir() if file_path.is_file()]
        if extension:
            files = [file_path for file_path in files if file_path.suffix.lower() == extension.lower()]
        if not files:
            raise FileNotFoundError(f"No files found in {directory}")
        return max(files, key=lambda file_path: file_path.stat().st_mtime)
