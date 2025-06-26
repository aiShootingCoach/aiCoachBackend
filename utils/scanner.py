import cv2
import mediapipe as mp
import numpy as np
import json
import math
import os
import numpy as np


def calculate_angle(first_point, mid_point, last_point):
    # Używamy tylko x i y, pomijamy z
    a = np.array([first_point.x, first_point.y])
    b = np.array([mid_point.x, mid_point.y])
    c = np.array([last_point.x, last_point.y])

    # Obliczamy wektory
    ba = a - b
    bc = c - b

    # Obliczamy kąt między wektorami
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # Zabezpieczenie przed błędami numerycznymi
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    angle = np.arccos(cosine_angle)
    angle = np.degrees(angle)

    return angle


def visualization(landmarks, image, mp_pose, mp_drawing, results=None):
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow("Pose Estimation", image)
        cv2.waitKey()
        # cv2.destroyAllWindows()
def to_json(landmarks):

    right_shoulder = landmarks[12]
    right_elbow = landmarks[14]
    right_wrist = landmarks[16]
    right_finger = landmarks[20]
    right_hip = landmarks[24]
    right_knee = landmarks[26]
    right_ankle = landmarks[28]
    # print(f"x: {right_shoulder.x}, y:{right_shoulder.y}, z:{right_shoulder.z}")
    # print(f"x: {right_elbow.x}, y:{right_elbow.y}, z:{right_elbow.z}")
    # print(f"x: {right_wrist.x}, y:{right_wrist.y}, z:{right_wrist.z}")
    right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    right_wrist_angle = calculate_angle(right_elbow, right_wrist, right_finger)
    right_shoulder_angle = calculate_angle(right_hip,right_shoulder,  right_elbow)
    right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

    left_shoulder = landmarks[11]
    left_elbow = landmarks[13]
    left_wrist = landmarks[15]
    left_finger = landmarks[19]
    left_hip = landmarks[23]
    left_knee = landmarks[25]
    left_ankle = landmarks[27]

    left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    left_wrist_angle = calculate_angle(left_elbow, left_wrist, left_finger)
    left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

    pose_data = {
        "right_elbow_angle": right_elbow_angle,
        "right_wrist_angle": right_wrist_angle,
        "right_shoulder_angle": right_shoulder_angle,
        "right_hip_angle": right_hip_angle,
        "right_knee_angle": right_knee_angle,
        "left_elbow_angle": left_elbow_angle,
        "left_wrist_angle": left_wrist_angle,
        "left_hip_angle": left_hip_angle,
        "left_knee_angle": left_knee_angle,
    }

    return pose_data


def scan(image_path):
    if not os.path.exists(image_path):
        print(f"Błąd: Plik nie istnieje: {image_path}")
        return None

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    image = cv2.imread(image_path)
    if image is None:
        print(f"Błąd: Nie można odczytać obrazu: {image_path}")
        return None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        print(f"Błąd: Nie wykryto punktów orientacyjnych w obrazie: {image_path}")
        return None

    pose_data = to_json(results.pose_landmarks.landmark)
    return pose_data


def main():
    scan("/home/kacper/zajecia_inf/PythonProject/data/training_data/gather.png")

if __name__ == "__main__":
    main()
