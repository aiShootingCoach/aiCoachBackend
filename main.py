import logging
import uvicorn
from fastapi import FastAPI

from routers import api

app = FastAPI()

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

app.include_router(api.router)

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "aiCoach!!!!"}