import logging
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from utils import film_scanner

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "user_shots"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_SIZE = 100 * 1024 * 1024  # 100MB

@router.get("/hello/", tags=["test"])
def hello_world():
    return "aiCoach says hello!!!"


@router.post("/uploadfile/")
async def upload_video(file: UploadFile = File(...)):
    """
    Uploads a video file to the server.

    The file is saved in the `app/data/user_shots` directory with a unique
    filename to prevent overwrites.
    """
    # Check if the uploaded file is a video
    logging.log(logging.INFO, file.content_type)
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")

    # Generate a unique filename using UUID to avoid collisions
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    destination_path = UPLOAD_DIR / unique_filename

    try:
        # Save the file in chunks to handle large files efficiently
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        # If anything goes wrong during file saving, return an error
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    finally:
        # Always close the file
        file.file.close()

    return film_scanner.scan_film(str(destination_path) )

    # Return the details of the uploaded file
    # return {
    #     "detail": "Video uploaded successfully!",
    #     "filename": unique_filename,
    #     "content_type": file.content_type,
    #     "saved_path": str(destination_path)  # Return path as a string
    # }