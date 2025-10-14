import logging
import shutil
import uuid
import base64
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from utils import api_additional
from utils.film_scanner import FilmScanner
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()


router = APIRouter()
FRAMES_DIR = Path(__file__).resolve().parent.parent.parent / "utils" / "frames"
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "user_shots"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_SIZE = 20 * 1024 * 1024  # 100MB

@router.get("/hello/", tags=["test"])
def hello_world():
    return "aiCoach says hello!!!"


@router.post("/uploadfile/")
async def upload_video(file: UploadFile = File(...)):
    # Check if the uploaded file is a video
    logging.log(logging.INFO, file.content_type)
    if file.content_type != "video/mp4" or file.size > MAX_SIZE:
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
    film_scanner = FilmScanner()
    return_json = film_scanner.scan_film(str(destination_path))

    frames  = api_additional.attach_frames(return_json)

    response = {
        "feedback": return_json['feedback'],
        "frames": frames
    }
    api_additional.clean()

    return response

app.include_router(router)