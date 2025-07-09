import os
from pathlib import Path

import cv2
from utils import scanner
import json

import mediapipe as mp



def scan_ex_data(path):
    # Scan exemplary images and save joint angles as JSON files
    save_path = Path(__file__).parent / "../data/exemplary_data"
    files = os.listdir(path)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    # Process each image in the directory
    for file in files:
        file_path = path + '/' + file
        # Scan the image to extract joint angles
        json_data = scanner.scan(file_path, pose)
        # Save the results to a JSON file
        save_file = save_path / f"{file[:-4]}.json"
        save_file = open(save_file, 'w')
        json_txt = json.dumps(json_data)
        save_file.write(json_txt)
        save_file.close()
    pose.close()
    return 0
