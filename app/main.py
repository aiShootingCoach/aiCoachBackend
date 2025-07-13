import logging
import uvicorn
from fastapi import FastAPI

app = FastAPI()

from app.routers import api

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
    "https://*",
    "https://spotonshot.com",
    "https://spotonshot.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("your_app:app", host="0.0.0.0", port=8000)

app.include_router(api.router)

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "aiCoach!!!!"}