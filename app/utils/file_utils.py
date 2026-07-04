from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from config import UPLOAD_DIR


class FileUtils:

    @staticmethod
    def save_upload(file: UploadFile) -> Path:

        extension = Path(file.filename).suffix

        file_path = UPLOAD_DIR / f"{uuid.uuid4()}{extension}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path