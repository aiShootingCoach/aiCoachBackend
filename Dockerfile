FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

USER root
RUN apt-get update && apt-get install -y libgl1 ffmpeg

COPY . /app

RUN pip install --progress-bar off -r /app/requirements.txt
