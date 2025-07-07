import os
from datetime import datetime
from pathlib import Path
import cv2
import json
import subprocess
import re
from utils import scanner, feedback, similarity
import mediapipe as mp

TOP_CAP = 100000
PERCENTAGE_BASE = 2500


def save_feedback_to_json(data, filename):
    with open(filename, 'w') as plik:
        json.dump(data, plik, indent=4)


def precantage_output(pose_data):
    follow = pose_data['follow'][1]
    gather = pose_data['gather'][1]
    loading = pose_data['loading'][1]
    release = pose_data['release'][1]
    follow = round((PERCENTAGE_BASE - follow) / PERCENTAGE_BASE*100)
    if follow < 0: follow = 0
    gather = round((PERCENTAGE_BASE - gather) / PERCENTAGE_BASE*100)
    if gather < 0: gather = 0
    loading = round((PERCENTAGE_BASE - loading) / PERCENTAGE_BASE*100)
    if loading < 0: loading = 0
    release = round((PERCENTAGE_BASE - release) / PERCENTAGE_BASE*100)
    if release < 0: release = 0
    out = {'follow': follow, 'gather': gather, 'loading': loading, 'release': release}
    return out


def compare_two():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    path1 = '/home/kacper/zajecia_inf/PythonProject/frames/20250626130022_1.jpg'
    path2 = '/home/kacper/zajecia_inf/PythonProject/frames/20250626130025_1.jpg'
    user_data1 = scanner.scan(path1, pose)
    user_data2 = scanner.scan(path2, pose)
    print(user_data1)
    print(user_data2)
    pose.close()


def differences(path, stage):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    if not path or path == "":
        print(f"Error: Invalid file path for stage {stage}")
        return None
    user_data = scanner.scan(path, pose)
    if user_data is None:
        print(f"Error: Failed to analyze frame for stage {stage}")
        return None
    exemplary_data_path = Path(__file__).parent / f"../data/exemplary_data/{stage}.json"
    if not os.path.exists(exemplary_data_path):
        print(f"Error: Exemplary data file for stage {stage} not found")
        return None
    try:
        with open(exemplary_data_path, 'r') as f:
            exemplar_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid format of exemplary data file for stage {stage}")
        return None
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
    }
    pose.close()
    return difference


def get_newest_file(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    if not files:
        return None
    newest_file = max(files, key=os.path.getmtime)
    return newest_file


def is_frame_path_used(most_similars_file, frame_path):
    for value in most_similars_file.values():
        if value[0] == frame_path:
            return True
    return False


def verify_frame_order(frame_stages):
    def get_frame_number(frame_path):
        if not frame_path:
            return -1
        return int(os.path.basename(frame_path).split('_')[1].split('.')[0])

    loading_frame = get_frame_number(frame_stages['loading'][0])
    gather_frame = get_frame_number(frame_stages['gather'][0])
    release_frame = get_frame_number(frame_stages['release'][0])
    follow_frame = get_frame_number(frame_stages['follow'][0])
    return (loading_frame < gather_frame < release_frame < follow_frame)


def find_next_best_frame(frame_scores, stage, used_frames, min_frame, max_frame):
    best_score = TOP_CAP
    best_frame = ""
    for frame_path, scores in frame_scores:
        frame_num = int(os.path.basename(frame_path).split('_')[1].split('.')[0])
        if (frame_path not in used_frames and
                min_frame <= frame_num <= max_frame):
            for filename, score in scores:
                if filename == f"{stage}.json" and score < best_score:
                    best_score = score
                    best_frame = frame_path
    return best_frame, best_score


def get_video_rotation(file_path):
    """Retrieve the rotation angle from video metadata using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_streams', '-select_streams', 'v:0', file_path],
            capture_output=True, text=True
        )
        output = result.stdout
        match = re.search(r'rotation=([-]?\d+)', output)
        if match:
            return int(match.group(1))
        return 0  # No rotation metadata found
    except subprocess.CalledProcessError:
        print(f"Error: Failed to run ffprobe on {file_path}")
        return 0


def scan_film(file_path, auto_rotate=True):
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

    # Get video rotation from metadata
    rotation = get_video_rotation(newest_file) if auto_rotate else 0
    rotation_map = {
        -90: cv2.ROTATE_90_CLOCKWISE,
        90: cv2.ROTATE_90_COUNTERCLOCKWISE,
        180: cv2.ROTATE_180,
        -180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_COUNTERCLOCKWISE,
        -270: cv2.ROTATE_90_CLOCKWISE
    }

    frame_scores = []
    # Initialize MediaPipe Pose and drawing utilities
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    try:
        frame_number = 0
        max_frames = 1000
        frame_skip = 5
        while frame_number < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply rotation to counteract metadata-driven rotation
            if rotation in rotation_map:
                frame = cv2.rotate(frame, rotation_map[rotation])
                print(f"klatka: {frame_number} (rotated {rotation} degrees)")

            print(f"klatka: {frame_number}")
            frames_dir = Path(__file__).parent / "frames"
            os.makedirs(frames_dir, exist_ok=True)
            frame_filename = f"frame_{frame_number:04d}.jpg"
            frame_path = os.path.join(frames_dir, frame_filename)
            cv2.imwrite(frame_path, frame)

            scan = scanner.scan(frame_path, pose)
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
        pose.close()

    # Pass 2: Assign frames to stages optimally
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        most_similars_file = {
            "loading": ["", TOP_CAP],
            "gather": ["", TOP_CAP],
            "release": ["", TOP_CAP],
            "follow": ["", TOP_CAP]
        }
        used_frames = set()
        for stage in ["loading", "gather", "release", "follow"]:
            best_score = TOP_CAP
            best_frame = ""
            for frame_path, scores in frame_scores:
                if frame_path not in used_frames:
                    for filename, score in scores:
                        if filename == f"{stage}.json" and score < best_score:
                            best_score = score
                            best_frame = frame_path
            if best_frame:
                most_similars_file[stage] = [best_frame, best_score]
                used_frames.add(best_frame)
        if verify_frame_order(most_similars_file):
            break
        worst_score = max(score for _, score in most_similars_file.values())
        worst_stage = next(stage for stage, (_, score) in most_similars_file.items()
                           if score == worst_score)
        used_frames.remove(most_similars_file[worst_stage][0])
        attempt += 1

    if attempt == max_attempts:
        print("Error: Failed to find optimal frame assignment")
    # for frame_path, _ in frame_scores:
    #     if frame_path not in used_frames and os.path.exists(frame_path):
    #         os.remove(frame_path)
    #         print(f"Removed frame: {os.path.basename(frame_path)}")


    all_feedback = []
    percentage = precantage_output(most_similars_file)
    tab_names = ["follow", "gather", "loading", "release"]
    for stage in tab_names:
        feedback.analyze_shot_form(differences(most_similars_file[stage][0], stage), stage)
        stage_feedback = {
            'stage': stage,
            'result': percentage[stage],
            'feedback': feedback.analyze_shot_form(differences(most_similars_file[stage][0], stage), stage)
        }
        all_feedback.append(stage_feedback)

    with open(feedback_file, 'w') as plik:
        json.dump(all_feedback, plik, indent=4)
    print("\nMost similar System: frames:")
    print(most_similars_file)
    print("\n")
    frames_end = [[most_similars_file['loading'][0],'loading'],[most_similars_file['gather'][0],'gather'],[most_similars_file['release'][0],'release'],[most_similars_file['follow'][0],'follow']]
    print(percentage)
    return_json = {'feedback':all_feedback, 'frames':frames_end}
    return return_json


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_shots_dir = os.path.join(os.path.dirname(current_dir), "data", "user_shots")
    scan_film(user_shots_dir)


if __name__ == '__main__':
    main()