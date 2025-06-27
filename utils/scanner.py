import cv2
import mediapipe as mp
import numpy as np
import json
import math
import os

from utils import similarity


def calculate_angle(first_point, mid_point, last_point):
    # Calculate the angle between three points using 2D coordinates (x, y)
    a = np.array([first_point.x, first_point.y])
    b = np.array([mid_point.x, mid_point.y])
    c = np.array([last_point.x, last_point.y])

    # Compute vectors
    ba = a - b
    bc = c - b

    # Calculate the cosine of the angle between vectors
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # Clip to avoid numerical errors
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    # Convert to degrees
    angle = np.arccos(cosine_angle)
    angle = np.degrees(angle)

    return angle

def visualization(landmarks, image, mp_pose, mp_drawing, results=None):
    # Visualize pose landmarks on the image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow("Pose Estimation", image)
        cv2.waitKey()
        # cv2.destroyAllWindows()

def to_json(landmarks):
    # Convert pose landmarks to a dictionary of joint angles
    right_shoulder = landmarks[12]
    right_elbow = landmarks[14]
    right_wrist = landmarks[16]
    right_finger = landmarks[20]
    right_hip = landmarks[24]
    right_knee = landmarks[26]
    right_ankle = landmarks[28]

    # Calculate right side angles
    right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    right_wrist_angle = calculate_angle(right_elbow, right_wrist, right_finger)
    right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
    right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

    left_shoulder = landmarks[11]
    left_elbow = landmarks[13]
    left_wrist = landmarks[15]
    left_finger = landmarks[19]
    left_hip = landmarks[23]
    left_knee = landmarks[25]
    left_ankle = landmarks[27]

    # Calculate left side angles
    left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    left_wrist_angle = calculate_angle(left_elbow, left_wrist, left_finger)
    left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

    # Store angles in a dictionary
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
    # Process an image to extract joint angles using MediaPipe Pose
    if not os.path.exists(image_path):
        print(f"Error: File does not exist: {image_path}")
        return None

    # Initialize MediaPipe Pose and drawing utilities
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    # Read and convert the image to RGB
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image: {image_path}")
        return None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print(f"Error: No landmarks detected in image: {image_path}")
        return None

    # Convert landmarks to joint angles
    pose_data = to_json(results.pose_landmarks.landmark)
    # visualization(pose_data, image, mp_pose, mp_drawing, results)
    return pose_data

def main():
    # Test function to scan specific images and compare with exemplary data
    print(similarity.compare_with_exemplary_data(scan("/home/kacper/zajecia_inf/PythonProject/frames/zr.png")))
    print(similarity.compare_with_exemplary_data(scan("/home/kacper/zajecia_inf/PythonProject/frames/frame_0020.jpg")))

if __name__ == "__main__":
    main()