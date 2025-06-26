import json
import numpy as np
import os
from typing import Dict, List, Union


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

            # Zbierz wszystkie dostępne kąty
            common_angles = []
            user_angles = []

            # Dynamicznie zbierz tylko te kąty, które są dostępne w obu plikach
            for key in ex_file.keys():
                if key.endswith('_angle') and key in user_data:
                    common_angles.append(ex_file[key])
                    user_angles.append(user_data[key])

            if not common_angles:
                print(f"Brak wspólnych kątów w pliku {file}")
                continue

            ex_angles = np.array(common_angles)
            user_angles = np.array(user_angles)

            differences = np.abs(ex_angles - user_angles)
            similarity_score = np.mean(differences)

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


def scan_film(directory):
    newest_file = get_newest_file(directory)
    most_similars_file = {
        "similar1": ["", 100],
        "similar2": ["", 100],
        "similar3": ["", 100],
        "similar4": ["", 100]
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
            
            # Skanowanie i zapisywanie danych w odpowiednim formacie
            scan_data = scanner.scan(frame_path)
            if scan_data:  # Sprawdzamy, czy dane zostały poprawnie zeskanowane
                similarity_scores = similarity.compare_with_exemplary_data(scan_data)  # Przekazujemy dane zamiast ścieżki
                
                # Zapisujemy dane do pliku JSON obok klatki
                json_filename = f"frame_{frame_number:04d}.json"
                json_path = os.path.join(frames_dir, json_filename)
                with open(json_path, 'w') as f:
                    json.dump(scan_data, f, indent=4)

                # Update most similar frames
                changed = False
                for i, (file, score) in enumerate(similarity_scores):
                    key = f"similar{i + 1}"
                    if score < most_similars_file[key][1]:
                        if most_similars_file[key][0] != "":
                            # Usuń stary plik obrazu i jego JSON
                            old_frame = most_similars_file[key][0]
                            old_json = old_frame.replace('.jpg', '.json')
                            if os.path.exists(old_frame):
                                os.remove(old_frame)
                            if os.path.exists(old_json):
                                os.remove(old_json)
                        most_similars_file[key] = [frame_path, score]
                        changed = True
                
                if not changed:
                    os.remove(frame_path)
                    os.remove(json_path)
                    print(f"Removed frame: {frame_filename}")
                else:
                    print(f"Saved frame: {frame_filename}")
            
            frame_number += frame_skip
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    finally:
        print("\nMost similar frames:")
        for key, value in most_similars_file.items():
            if value[0]:
                print(f"{key}: {value[0]} (similarity score: {value[1]:.2f})")

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()