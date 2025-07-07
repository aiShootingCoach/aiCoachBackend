import json
from pathlib import Path

import numpy as np
import os
from typing import Dict, List, Union

# Define weights for each joint angle across shooting stages
weights = {
    "Load": {
        "Right": {
            "Wrist": 4,
            "Elbow": 7,
            "Shoulder": 9,
            "Hip": 8,
            "Knee": 7
        },
        "Left": {
            "Wrist": 3,
            "Elbow": 6,
            "Shoulder": 7,
            "Hip": 8,
            "Knee": 7
        }
    },
    "Gather": {
        "Right": {
            "Wrist": 8,
            "Elbow": 10,
            "Shoulder": 8,
            "Hip": 9,
            "Knee": 9
        },
        "Left": {
            "Wrist": 4,
            "Elbow": 8,
            "Shoulder": 7,
            "Hip": 9,
            "Knee": 9
        }
    },
    "Release": {
        "Right": {
            "Wrist": 10,
            "Elbow": 9,
            "Shoulder": 10,
            "Hip": 5,
            "Knee": 6
        },
        "Left": {
            "Wrist": 5,
            "Elbow": 6,
            "Shoulder": 7,
            "Hip": 5,
            "Knee": 6
        }
    },
    "FollowThrough": {
        "Right": {
            "Wrist": 9,
            "Elbow": 9 ,
            "Shoulder": 9,
            "Hip": 6,
            "Knee": 5
        },
        "Left": {
            "Wrist": 9,
            "Elbow": 9,
            "Shoulder": 9,
            "Hip": 6,
            "Knee": 5
        }
    }
}

def read_json_file(file_path: str) -> dict:
    # Read and parse a JSON file
    with open(file_path, 'r') as file:
        return json.load(file)

def print_json_structure():
    # Print the structure (keys) of all JSON files in the exemplary data directory
    ex_path =Path(__file__).parent / f"../data/exemplary_data/"
    for file in os.listdir(ex_path):
        if file.endswith('.json'):
            data = read_json_file(os.path.join(ex_path, file))
            print("Available fields:", list(data.keys()))

def get_weight(angle_name, stage_name) -> float:
    # Retrieve the weight for a specific angle and stage
    stage_mapping = {
        'loading.json': 'Load',
        'gather.json': 'Gather',
        'release.json': 'Release',
        'follow.json': 'FollowThrough'
    }

    # Determine side (Right/Left) based on angle name
    side = 'Right' if angle_name.startswith('right_') else 'Left'

    # Map angle types to weight dictionary keys
    angle_type_mapping = {
        'wrist': 'Wrist',
        'elbow': 'Elbow',
        'shoulder': 'Shoulder',
        'hip': 'Hip',
        'knee': 'Knee'
    }

    # Extract angle type from angle name (e.g., 'right_elbow_angle' -> 'elbow')
    angle_type = angle_name.split('_')[1].split('_')[0]

    # Return default weight if stage not found
    if stage_name not in stage_mapping:
        return 1

    stage = stage_mapping[stage_name]
    angle_type = angle_type_mapping.get(angle_type, '')

    try:
        return weights[stage][side][angle_type]
    except KeyError:
        return 1  # Default weight in case of error

def compare_with_exemplary_data(user_data: dict) -> List[tuple]:
    # Compare user joint angles with exemplary data and compute similarity scores
    # ex_path = '/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/'
    ex_path = Path(__file__).parent / "../data/exemplary_data"
    files = os.listdir(ex_path)
    similarity_results = []

    # Print System: Print structure of the first exemplary data file


    if files:
        first_file = read_json_file(os.path.join(ex_path, files[0]))
        print("Structure of first file:", list(first_file.keys()))

    # Process each exemplary data file
    for file in reversed(files):
        if not file.endswith('.json'):
            continue

        try:
            ex_file = read_json_file(os.path.join(ex_path, file))

            # Collect common angles between user and exemplary data
            common_angles = []
            user_angles = []

            for key in ex_file.keys():
                if key.endswith('_angle') and key in user_data:
                    common_angles.append(ex_file[key])
                    user_angles.append(user_data[key])

            if not common_angles:
                print(f"No common angles in file {file}")
                continue

            # Calculate weighted similarity score (weighted mean squared error)
            full_weight = 0
            similarity_score = 0
            for user_angle, compare_angle in zip(user_angles, common_angles):
                weight = get_weight(key, file)
                similarity_score += (user_angle - compare_angle) * (user_angle - compare_angle) * weight * weight
                full_weight += weight * weight

            similarity_score = similarity_score / full_weight

            if user_data['right_top_diffrence'] != ex_file['right_top_diffrence'] or user_data['left_top_diffrence'] != ex_file['left_top_diffrence']:
                similarity_score = 10000


            similarity_results.append((file, similarity_score))

        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
            continue

    return similarity_results

def main():
    # Test function to compare test data with exemplary data
    test_data = {
        'right_elbow_angle': 111.23,
        'right_wrist_angle': 171.75,
        'right_shoulder_angle': 29.27,
        'right_hip_angle': 139.86,
        'right_knee_angle': 137.18,
        'left_elbow_angle': 133.93,
        'left_wrist_angle': 156.84,
        'left_hip_angle': 113.99,
        'left_knee_angle': 123.23
    }

    try:
        scores = compare_with_exemplary_data(test_data)
        if scores:
            print("\nSimilarity results (lower score = better match):")
            print("-" * 50)
            for filename, score in scores:
                print(f"{filename}: {score:.2f}")
        else:
            print("No comparison results found")

    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == '__main__':
    main()