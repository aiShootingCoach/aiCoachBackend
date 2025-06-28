import os
from datetime import datetime
from pathlib import Path

import cv2
import json
from utils import scanner, feedback, similarity


def save_feedback_to_json(data, filename):
    with open(filename, 'w') as plik:
        json.dump(data, plik, indent=4)

def precantage_output(pose_data):
     follow = pose_data['follow'][1]
     gather = pose_data['gather'][1]
     loading = pose_data['loading'][1]
     release = pose_data['release'][1]
     follow = format((10000 - follow)/10000,'.2%')
     gather = format((10000 - gather)/10000,'.2%')
     loading = format((10000 - loading)/10000,'.2%')
     release = format((10000 - release)/10000,'.2%')
     out = {'follow': follow, 'gather': gather, 'loading': loading, 'release': release}
     return out

def compare_two():
    # Compare two specific frames for testing purposes
    path1 = '/home/kacper/zajecia_inf/PythonProject/frames/20250626130022_1.jpg'
    path2 = '/home/kacper/zajecia_inf/PythonProject/frames/20250626130025_1.jpg'
    user_data1 = scanner.scan(path1)
    user_data2 = scanner.scan(path2)
    print(user_data1)
    print(user_data2)

def differences(path, stage):
    # Calculate the difference in joint angles between a frame and exemplary data for a given stage
    if not path or path == "":
        print(f"Error: Invalid file path for stage {stage}")
        return None

    # Scan the frame to get user joint angles
    user_data = scanner.scan(path)
    if user_data is None:
        print(f"Error: Failed to analyze frame for stage {stage}")
        return None

    # Load exemplary data for the specified stage
    exemplary_data_path =Path(__file__).parent / f"../data/exemplary_data/{stage}.json"
    if not os.path.exists(exemplary_data_path):
        print(f"Error: Exemplary data file for stage {stage} not found")
        return None

    try:
        with open(exemplary_data_path, 'r') as f:
            exemplar_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid format of exemplary data file for stage {stage}")
        return None

    # Compute angle differences between user and exemplary data
    difference = {
        "right_elbow_angle": user_data["right_elbow_angle"] - exemplar_data["right_elbow_angle"],
        "right_wrist_angle": user_data["right_wrist_angle"] - exemplar_data["right_wrist_angle"],
        "right_shoulder_angle": user_data["right_shoulder_angle"] - exemplar_data["right_shoulder_angle"],
        "right_hip_angle": user_data["right_hip_angle"] - exemplar_data["right_hip_angle"],
        "right_knee_angle": user_data["right_knee_angle"] - exemplar_data["right_knee_angle"],
        "left_elbow_angle": user_data["left_elbow_angle"] - exemplar_data["left_elbow_angle"],
        "left_wrist_angle": user_data["left_wrist_angle"] - exemplar_data["left_wrist_angle"],
        "left_hip_angle": user_data["left_hip_angle"] - exemplar_data["left_hip_angle"],
        "left_knee_angle": user_data["left_knee_angle"] - exemplar_data["left_knee_angle"],
        # "left_shoulder_angle": user_data["left_shoulder_angle"] - exemplar_data["left_shoulder_angle"]
    }

    return difference

def get_newest_file(directory):
    # Retrieve the most recently modified file in the specified directory
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    if not files:
        return None
    newest_file = max(files, key=os.path.getmtime)
    return newest_file

def is_frame_path_used(most_similars_file, frame_path):
    # Check if a frame has already been assigned to any stage
    for value in most_similars_file.values():
        if value[0] == frame_path:
            return True
    return False

def scan_film(file_path):
    current_dir = Path(__file__).resolve().parent.parent
    feedback_file = current_dir / "data" / "feedback.json"

    feedback_file.parent.mkdir(parents=True, exist_ok=True)

    newest_file = file_path
    if newest_file is None:
        print("Błąd: Brak plików wideo w katalogu")
        return

    cap = cv2.VideoCapture(newest_file)
    if not cap.isOpened():
        print("Błąd: Nie można otworzyć pliku wideo")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Check if video is in portrait mode (typical for phone videos)
    is_portrait = height > width

    frame_scores = []
    try:
        frame_number = 0
        max_frames = 1000
        frame_skip = 2
        while frame_number < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Rotate frame if video is in portrait mode
            if is_portrait:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            
            print(f"klatka: {frame_number}")
            # parent_dir = os.path.dirname(os.path.dirname(directory))
            frames_dir = Path(__file__).parent / "frames"

            os.makedirs(frames_dir, exist_ok=True)
            frame_filename = f"frame_{frame_number:04d}.jpg"
            frame_path = os.path.join(frames_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            
            # Rest of the code remains the same
            scan = scanner.scan(frame_path)
            if scan is None:
                if os.path.exists(frame_path):
                    os.remove(frame_path)
                print(f"Pominięto klatkę {frame_number} - błąd skanowania")
                frame_number += frame_skip
                continue

            similarity_scores = similarity.compare_with_exemplary_data(scan)
            print(similarity_scores)
            frame_scores.append((frame_path, similarity_scores))
            frame_number += frame_skip
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    finally:
        cap.release()

    # Pass 2: Assign frames to stages optimally
    most_similars_file = {
        "follow": ["", 100000],
        "gather": ["", 100000],
        "loading": ["", 100000],
        "release": ["", 100000]
    }
    used_frames = set()
    tab_names = ["follow", "gather", "loading", "release"]

    # Assign the best frame to each stage based on lowest similarity score
    for stage in tab_names:
        best_score = 100000
        best_frame = ""
        for frame_path, scores in frame_scores:
            for filename, score in scores:
                if filename == f"{stage}.json" and score < best_score and frame_path not in used_frames:
                    best_score = score
                    best_frame = frame_path
        if best_frame:
            most_similars_file[stage] = [best_frame, best_score]
            used_frames.add(best_frame)
        else:
            print(f"No suitable frame found for stage {stage}")

    # Clean up unused frames
    for frame_path, _ in frame_scores:
        if frame_path not in used_frames and os.path.exists(frame_path):
            os.remove(frame_path)
            print(f"Removed frame: {os.path.basename(frame_path)}")
    all_feedback = []
    percentage = precantage_output(most_similars_file)
    for stage in tab_names:
        feedback.analyze_shot_form(differences(most_similars_file[stage][0], stage), stage)
        stage_feedback = {
            'stage': stage,
            'result': percentage[stage],
            'feedback':  feedback.analyze_shot_form(differences(most_similars_file[stage][0], stage), stage)
        }
        all_feedback.append(stage_feedback)

    with open(feedback_file, 'w') as plik:
        json.dump(all_feedback, plik, indent=4)
    print("\nMost similar System: frames:")
    print(most_similars_file)
    print("\n")
    print(percentage)
    return all_feedback

def main():
    # Main function to initiate video scanning
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_shots_dir = os.path.join(os.path.dirname(current_dir), "data", "user_shots")
    scan_film(user_shots_dir)

if __name__ == '__main__':
    main()