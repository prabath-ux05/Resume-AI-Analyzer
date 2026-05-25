import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

# Ensure the upload directory exists upon module load
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile, destination_folder: str = UPLOAD_DIR) -> str:
    """
    Saves an uploaded file to the destination folder.
    Returns the file path.
    """
    file_path = os.path.join(destination_folder, upload_file.filename)
    # Using 'with open' to write the file in chunks
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path
