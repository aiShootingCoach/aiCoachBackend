import os
from datetime import datetime
import cv2
import json
import scanner
import similarity
import feedback


def differences(path, stage):
    user_data = scanner.scan(path)
    with open(f'/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/{stage}.json', 'r') as f:
        exemplar_data = json.load(f)

    difference = {
        "right_elbow_angle": user_data["right_elbow_angle"] - exemplar_data["right_elbow_angle"],
        "right_wrist_angle": user_data["right_wrist_angle"] - exemplar_data["right_wrist_angle"],
        "right_shoulder_angle": user_data["right_shoulder_angle"] - exemplar_data["right_shoulder_angle"],
        "right_hip_angle": user_data["right_hip_angle"] - exemplar_data["right_hip_angle"],
        "right_knee_angle": user_data["right_knee_angle"] - exemplar_data["right_knee_angle"],
        "left_elbow_angle": user_data["left_elbow_angle"] - exemplar_data["left_elbow_angle"],
        "left_wrist_angle": user_data["left_wrist_angle"] - exemplar_data["left_wrist_angle"],
        "left_hip_angle": user_data["left_hip_angle"] - exemplar_data["left_hip_angle"],
        "left_knee_angle": user_data["left_knee_angle"] - exemplar_data["left_knee_angle"]
    }

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


def scan_film(directory):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    feedback_file = os.path.join(os.path.dirname(current_dir), "data", "feedback.json")

    newest_file = get_newest_file(directory)
    most_similars_file = {
        "follow": ["", 100],
        "gather": ["", 100],
        "loading": ["", 100],
        "release": ["", 100]  # Fixed typo in "release"
    }
    if newest_file is None:
        return

    cap = cv2.VideoCapture(newest_file)
    if not cap.isOpened():
        print("Błąd: Nie można otworzyć pliku wideo")
        return

    try:
        frame_number = 0
        max_frames = 1000
        frame_skip = 5
        while frame_number < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            print(f"klatka: {frame_number}")
            parent_dir = os.path.dirname(os.path.dirname(directory))
            frames_dir = os.path.join(parent_dir, "frames")
            os.makedirs(frames_dir, exist_ok=True)
            frame_filename = f"frame_{frame_number:04d}.jpg"
            frame_path = os.path.join(frames_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            scan = scanner.scan(frame_path)
            print(scan)
            similarity_scores = similarity.compare_with_exemplary_data(scan)

            # Update most similar frames
            changed = False
            tab_names = ["follow", "gather", "loading", "release"]
            for i, (filename, score) in enumerate(similarity_scores):  # Rozpakowanie krotki
                key = tab_names[i]
                if score < most_similars_file[key][1] and not is_frame_path_used(most_similars_file, frame_path):
                    if most_similars_file[key][0] != "" and os.path.exists(most_similars_file[key][0]) and most_similars_file[key][0] != frame_path:
                        os.remove(most_similars_file[key][0])
                    most_similars_file[key] = [frame_path, score]
                    changed = True

            if not changed:
                os.remove(frame_path)
                print(f"Removed frame: {frame_filename}")
            else:
                print(f"Saved frame: {frame_filename}")

            frame_number += frame_skip
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    finally:
        print("\nMost similar frames:")

        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "shots": {}
        }

        for key, value in most_similars_file.items():
            shot_feedback = feedback.analyze_shot_form(differences(value[0], key), key)
            feedback_data["shots"][key] = {
                "frame_path": value[0],
                "similarity_score": value[1],
                "feedback": shot_feedback
            }

        try:
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            else:
                existing_data = []

            existing_data.append(feedback_data)

            with open(feedback_file, 'w') as f:
                json.dump(existing_data, f, indent=4)

        except Exception as e:
            print(f"Error saving feedback: {str(e)}")

        cap.release()
        cv2.destroyAllWindows()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_shots_dir = os.path.join(os.path.dirname(current_dir), "data", "user_shots")
    scan_film(user_shots_dir)


if __name__ == '__main__':
    main()
