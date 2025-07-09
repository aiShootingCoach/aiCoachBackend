import base64
import logging
from pathlib import Path

FRAMES_DIR = Path(__file__).resolve().parent.parent.parent / "utils" / "frames"
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "data" / "user_shots"

def clean():
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

def attach_frames(return_json: dict):
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
    return frames