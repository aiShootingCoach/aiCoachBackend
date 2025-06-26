import json
import numpy as np
import os
from typing import Dict, List, Union

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
                "Wrist": 5,
                "Elbow": 7,
                "Shoulder": 8,
                "Hip": 9,
                "Knee": 9
            },
            "Left": {
                "Wrist": 4,
                "Elbow": 6,
                "Shoulder": 7,
                "Hip": 9,
                "Knee": 9
            }
        },
        "Release": {
            "Right": {
                "Wrist": 10,
                "Elbow": 9,
                "Shoulder": 8,
                "Hip": 7,
                "Knee": 6
            },
            "Left": {
                "Wrist": 5,
                "Elbow": 6,
                "Shoulder": 7,
                "Hip": 6,
                "Knee": 6
            }
        },
        "FollowThrough": {
            "Right": {
                "Wrist": 9,
                "Elbow": 8,
                "Shoulder": 9,
                "Hip": 6,
                "Knee": 5
            },
            "Left": {
                "Wrist": 4,
                "Elbow": 5,
                "Shoulder": 6,
                "Hip": 6,
                "Knee": 5
            }
        }
    }
def read_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)


def print_json_structure():
    """Funkcja pomocnicza do wyświetlenia struktury plików JSON"""
    ex_path = '/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/'
    for file in os.listdir(ex_path):
        if file.endswith('.json'):
            print(f"\nZawartość pliku {file}:")
            data = read_json_file(os.path.join(ex_path, file))
            print("Dostępne pola:", list(data.keys()))


def get_weight(angle_name, stage_name) -> float:
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

    # Wyciągnięcie typu kąta z nazwy
    angle_type = angle_name.split('_')[1].split('_')[0]  # np. z 'right_elbow_angle' otrzymamy 'elbow'

    if stage_name not in stage_mapping:
        return 1  # domyślna waga jeśli nie znaleziono odpowiednika

    stage = stage_mapping[stage_name]
    angle_type = angle_type_mapping.get(angle_type, '')

    try:
        return weights[stage][side][angle_type]
    except KeyError:
        return 1  # domyślna waga w przypadku błędu


def compare_with_exemplary_data(user_data: dict) -> List[tuple]:
    ex_path = '/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/'
    files = os.listdir(ex_path)
    similarity_results = []


    # Najpierw wydrukujmy strukturę pierwszego pliku
    if files:
        first_file = read_json_file(os.path.join(ex_path, files[0]))
        print("Struktura pierwszego pliku:", list(first_file.keys()))

    for file in files:
        if not file.endswith('.json'):
            continue

        try:
            ex_file = read_json_file(os.path.join(ex_path, file))

            common_angles = []
            user_angles = []

            for key in ex_file.keys():
                if key.endswith('_angle') and key in user_data:
                    common_angles.append(ex_file[key])
                    user_angles.append(user_data[key])

            if not common_angles:
                print(f"Brak wspólnych kątów w pliku {file}")
                continue
            full_weight = 0
            similarity_score = 0
            for user_angle, compare_angle in zip(user_angles, common_angles):
                weight = get_weight(key, file)  # gdzie key to nazwa kąta (np. 'right_elbow_angle'), a file to nazwa pliku
                similarity_score += np.sqrt(abs(user_angle * user_angle - compare_angle * compare_angle))*weight
                full_weight+=weight


            similarity_score = similarity_score/full_weight

            similarity_results.append((file, similarity_score))

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {file}: {str(e)}")
            continue

    return similarity_results


def main():
    # Najpierw wyświetl strukturę plików
    print("Sprawdzanie struktury plików przykładowych:")
    print_json_structure()

    # Przykładowe dane testowe - dostosujemy je po zobaczeniu rzeczywistej struktury
    test_data = {'right_elbow_angle': 111.23, 'right_wrist_angle': 171.75, 'right_shoulder_angle': 29.27, 'right_hip_angle': 139.86, 'right_knee_angle': 137.18, 'left_elbow_angle': 133.93, 'left_wrist_angle': 156.84, 'left_hip_angle': 113.99, 'left_knee_angle': 123.23}


    try:
        scores = compare_with_exemplary_data(test_data)
        if scores:
            print("\nWyniki podobieństwa (niższa wartość = większe podobieństwo):")
            print("-" * 50)
            for filename, score in scores:
                print(f"{filename}: {score:.2f}")
        else:
            print("Nie znaleziono żadnych wyników porównania")

    except Exception as e:
        print(f"Błąd podczas testu: {str(e)}")

if __name__ == '__main__':
    main()