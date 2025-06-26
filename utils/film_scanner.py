import os
from datetime import datetime
import cv2
import json
import scanner
import similarity
import feedback

def compare_two():
    path1 = '/home/kacper/zajecia_inf/PythonProject/frames/20250626130022_1.jpg'
    path2 = '/home/kacper/zajecia_inf/PythonProject/frames/20250626130025_1.jpg'
    user_data1 = scanner.scan(path1)
    user_data2 = scanner.scan(path2)
    print(user_data1)
    print(user_data2)
    # difference = {
    #     "right_elbow_angle": user_data["right_elbow_angle"] - exemplar_data["right_elbow_angle"],
    #     "right_wrist_angle": user_data["right_wrist_angle"] - exemplar_data["right_wrist_angle"],
    #     "right_shoulder_angle": user_data["right_shoulder_angle"] - exemplar_data["right_shoulder_angle"],
    #     "right_hip_angle": user_data["right_hip_angle"] - exemplar_data["right_hip_angle"],
    #     "right_knee_angle": user_data["right_knee_angle"] - exemplar_data["right_knee_angle"],
    #     "left_elbow_angle": user_data["left_elbow_angle"] - exemplar_data["left_elbow_angle"],
    #     "left_wrist_angle": user_data["left_wrist_angle"] - exemplar_data["left_wrist_angle"],
    #     "left_hip_angle": user_data["left_hip_angle"] - exemplar_data["left_hip_angle"],
    #     "left_knee_angle": user_data["left_knee_angle"] - exemplar_data["left_knee_angle"]
    # }
    # print(difference)
    # print(similarity.compare_with_exemplary_data(user_data))


def differences(path, stage):
    if not path or path == "":
        print(f"Błąd: Nieprawidłowa ścieżka do pliku dla etapu {stage}")
        return None

    user_data = scanner.scan(path)
    if user_data is None:
        print(f"Błąd: Nie udało się przeanalizować klatki dla etapu {stage}")
        return None

    exemplary_data_path = f'/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/{stage}.json'
    if not os.path.exists(exemplary_data_path):
        print(f"Błąd: Brak pliku wzorcowego dla etapu {stage}")
        return None

    try:
        with open(exemplary_data_path, 'r') as f:
            exemplar_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Błąd: Nieprawidłowy format pliku wzorcowego dla etapu {stage}")
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
        "follow": ["", 1000],
        "gather": ["", 1000],
        "loading": ["", 1000],
        "release": ["", 1000]
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
        frame_skip = 2
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
            if scan is None:
                # Jeśli skanowanie się nie powiodło, usuń klatkę i przejdź do następnej
                if os.path.exists(frame_path):
                    os.remove(frame_path)
                print(f"Pominięto klatkę {frame_number} - błąd skanowania")
                frame_number += frame_skip
                continue

            print(scan)
            similarity_scores = similarity.compare_with_exemplary_data(scan)

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
        print(most_similars_file)

        # feedback_data = {
        #     "timestamp": datetime.now().isoformat(),
        #     "shots": {}
        # }
        #
        # for key, value in most_similars_file.items():
        #     if value[0]:
        #         diff_result = differences(value[0], key)
        #         if diff_result is None:
        #             feedback_data["shots"][key] = {
        #                 "frame_path": value[0],
        #                 "similarity_score": value[1],
        #                 "feedback": "Nie udało się przeanalizować klatki"
        #             }
        #             continue
        #
        #         shot_feedback = feedback.analyze_shot_form(diff_result, key)
        #         feedback_data["shots"][key] = {
        #             "frame_path": value[0],
        #             "similarity_score": value[1],
        #             "feedback": shot_feedback
        #         }
        #
        # try:
        #     if os.path.exists(feedback_file):
        #         with open(feedback_file, 'r') as f:
        #             existing_data = json.load(f)
        #         if not isinstance(existing_data, list):
        #             existing_data = [existing_data]
        #     else:
        #         existing_data = []
        #
        #     existing_data.append(feedback_data)
        #
        #     with open(feedback_file, 'w') as f:
        #         json.dump(existing_data, f, indent=4)
        #
        # except Exception as e:
        #     print(f"Error saving feedback: {str(e)}")
        #
        # cap.release()
        # cv2.destroyAllWindows()


def main():
    # compare_two()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_shots_dir = os.path.join(os.path.dirname(current_dir), "data", "user_shots")
    scan_film(user_shots_dir)


if __name__ == '__main__':
    main()