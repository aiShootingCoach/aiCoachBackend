import json
from pathlib import Path

import numpy as np
import os
from typing import Dict, List, Union
import logging

logger = logging.getLogger(__name__)

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

class Similarity:
    def __init__(self, user_data: dict):
        self.user_data = user_data

    @staticmethod
    def read_json_file(file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def print_json_structure():
        ex_path = Path(__file__).parent / "../data/exemplary_data/"
        for file in os.listdir(ex_path):
            if file.endswith('.json'):
                data = Similarity.read_json_file(os.path.join(ex_path, file))  # Use class name for static call
                logger.info("Available fields: %s", list(data.keys()))

    @staticmethod
    def get_weight(angle_name: str, stage_name: str) -> float:
        stage_mapping = {
            'loading.json': 'Load',
            'gather.json': 'Gather',
            'release.json': 'Release',
            'follow.json': 'FollowThrough'
        }

        side = 'Right' if angle_name.startswith('right_') else 'Left'

        angle_type_mapping = {
            'wrist': 'Wrist',
            'elbow': 'Elbow',
            'shoulder': 'Shoulder',
            'hip': 'Hip',
            'knee': 'Knee'
        }

        angle_type = angle_name.split('_')[1]

        if stage_name not in stage_mapping:
            return 1

        stage = stage_mapping[stage_name]
        angle_type = angle_type_mapping.get(angle_type, '')

        try:
            return weights[stage][side][angle_type]
        except KeyError:
            return 1

    def compare_with_exemplary_data(self) -> List[tuple]:
        ex_path = Path(__file__).parent / "../data/exemplary_data"
        files = os.listdir(ex_path)
        similarity_results = []

        if files:
            first_file = self.read_json_file(os.path.join(ex_path, files[0]))
            logger.info("Structure of first file: %s", list(first_file.keys()))

        for file in reversed(files):
            if not file.endswith('.json'):
                continue

            try:
                ex_file = self.read_json_file(os.path.join(ex_path, file))

                # Collect common angles with keys
                common = [
                    (key, ex_file[key], self.user_data[key])
                    for key in ex_file
                    if key.endswith('_angle') and key in self.user_data
                ]

                if not common:
                    logger.info(f"No common angles in file {file}")
                    continue

                # Calculate weighted similarity score
                full_weight = 0
                similarity_score = 0
                for key, compare_angle, user_angle in common:
                    weight = Similarity.get_weight(key, file)  # Static call
                    similarity_score += (user_angle - compare_angle) ** 2 * weight ** 2
                    full_weight += weight ** 2

                similarity_score = similarity_score / full_weight if full_weight > 0 else 0

                if (self.user_data.get('right_top_difference', 0) != ex_file.get('right_top_difference', 0) or
                    self.user_data.get('left_top_difference', 0) != ex_file.get('left_top_difference', 0)):
                    similarity_score = 10000

                similarity_results.append((file, similarity_score))

            except Exception as e:
                logger.info(f"Error processing file {file}: {str(e)}")
                continue

        return similarity_results

# def main():
#     # Test function to compare test data with exemplary data
#     test_data = {
#         'right_elbow_angle': 111.23,
#         'right_wrist_angle': 171.75,
#         'right_shoulder_angle': 29.27,
#         'right_hip_angle': 139.86,
#         'right_knee_angle': 137.18,
#         'left_elbow_angle': 133.93,
#         'left_wrist_angle': 156.84,
#         'left_hip_angle': 113.99,
#         'left_knee_angle': 123.23
#     }
#
#     try:
#         scores = compare_with_exemplary_data(test_data)
#         if scores:
#             logger.info("\nSimilarity results (lower score = better match):")
#             logger.info("-" * 50)
#             for filename, score in scores:
#                 logger.info(f"{filename}: {score:.2f}")
#         else:
#             logger.info("No comparison results found")
#
#     except Exception as e:
#         logger.error(f"Error during test: {str(e)}")
#
# if __name__ == '__main__':
#     main()