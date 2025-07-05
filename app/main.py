import logging
import uvicorn
from fastapi import FastAPI

app = FastAPI()

from app.routers import api

if __name__ == "__main__":
    uvicorn.run("your_app:app", host="0.0.0.0", port=8000)

app.include_router(api.router)

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "aiCoach!!!!"}