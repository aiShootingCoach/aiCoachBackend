import logging
import shutil
import uuid
import base64
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from utils import film_scanner
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()


router = APIRouter()
FRAMES_DIR = Path(__file__).resolve().parent.parent.parent / "utils" / "frames"
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "user_shots"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_SIZE = 2 * 1024 * 1024  # 100MB

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

    return_json = film_scanner.scan_film(str(destination_path))

    frames = []
    for frame_path in return_json['frames']:
        try:
            with open(frame_path[0], 'rb') as file:
                img_data = file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                add = [img_base64, frame_path[1]]
                frames.append(add)
        except Exception as e:
            logging.error(f"Error reading frame {frame_path}: {e}")
            add = ['null', frame_path[1]]
            frames.append(add)
            continue

    response = {
        "feedback": return_json['feedback'],
        "frames": frames
    }

    for file_path in FRAMES_DIR.glob("*.jpg"):
        try:
            file_path.unlink()
            logging.info(f"Deleted frame: {file_path}")
        except Exception as e:
            logging.error(f"Error deleting frame {file_path}: {e}")

        # Remove all files in the user_shots directory
    for file_path in UPLOAD_DIR.glob("*.mp4"):
        try:
            file_path.unlink()
            logging.info(f"Deleted video: {file_path}")
        except Exception as e:
            logging.error(f"Error deleting video {file_path}: {e}")

    return response

app.include_router(router)