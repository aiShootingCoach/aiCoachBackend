from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import film_scanner



app = FastAPI()
upload_dir = "data/user_shots/"
os.makedirs(upload_dir, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/uploadfile/")
async def upload_use_shot(file: UploadFile = File(...)):
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")

    max_size = 100 * 1024 * 1024  # 100MB
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=400, detail="File too large, max 100MB")

    try:
        filename = file.filename
        file_path = os.path.join(upload_dir, filename)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)
        return film_scanner.scan_film(file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")