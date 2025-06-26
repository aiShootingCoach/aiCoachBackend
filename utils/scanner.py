import cv2
import mediapipe as mp
import numpy as np
import json
import math

import numpy as np


def calculate_angle(a, b, c, min_visibility=0.5, use_world_landmarks=False):
    """
    Calculate the angle between three points in 3D space.

    Args:
        a, b, c: Landmark objects (from pose_landmarks or pose_world_landmarks).
        min_visibility: Minimum visibility threshold for reliable points.
        use_world_landmarks: If True, use pose_world_landmarks (metric coordinates).

    Returns:
        Angle in degrees, or None if points are unreliable.
    """
    # Check visibility
    if (a.visibility < min_visibility or
            b.visibility < min_visibility or
            c.visibility < min_visibility):
        return None  # Skip if any point has low visibility

    # Use world landmarks (meters) or normalized landmarks
    if use_world_landmarks:
        a_vec = np.array([a.x, a.y, a.z])
        b_vec = np.array([b.x, b.y, b.z])
        c_vec = np.array([c.x, c.y, c.z])
    else:
        a_vec = np.array([a.x, a.y, a.z])
        b_vec = np.array([b.x, b.y, b.z])
        c_vec = np.array([c.x, c.y, c.z])

    # Create vectors
    ab = a_vec - b_vec
    bc = c_vec - b_vec

    # Check for near-zero vectors
    magnitude_ab = np.linalg.norm(ab)
    magnitude_bc = np.linalg.norm(bc)
    if magnitude_ab < 1e-6 or magnitude_bc < 1e-6:
        return None  # Avoid division by zero

    # Calculate angle
    dot_product = np.dot(ab, bc)
    cosine_angle = dot_product / (magnitude_ab * magnitude_bc)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Ensure numerical stability
    angle = np.arccos(cosine_angle)
    angle_degrees = np.degrees(angle)

    return round(angle_degrees, 2)
def visualization(landmarks, image, mp_pose, mp_drawing, results=None):
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow("Pose Estimation", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
def to_json(landmarks):

    right_shoulder = landmarks[12]
    right_elbow = landmarks[14]
    right_wrist = landmarks[16]
    right_finger = landmarks[20]
    right_hip = landmarks[24]
    right_knee = landmarks[26]
    right_ankle = landmarks[28]

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
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose.process(image_rgb)
    pose_data = to_json(results.pose_landmarks.landmark)
    # print(pose_data)
    return pose_data




def main():
    scan("/home/kacper/zajecia_inf/PythonProject/data/training_data/gather7.png")

if __name__ == "__main__":
    main()
