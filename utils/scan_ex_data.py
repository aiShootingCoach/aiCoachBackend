import os
import cv2
import scanner
import json


def scan_ex_data(path):
    # Scan exemplary images and save joint angles as JSON files
    save_path = '/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/'
    files = os.listdir(path)

    # Process each image in the directory
    for file in files:
        file_path = path + '/' + file
        # Scan the image to extract joint angles
        json_data = scanner.scan(file_path)
        # Save the results to a JSON file
        save_file = save_path + file[:-4] + '.json'
        save_file = open(save_file, 'w')
        json_txt = json.dumps(json_data)
        save_file.write(json_txt)
        save_file.close()
    return 0


if __name__ == '__main__':
    # Run the scanning process for exemplary data
    scan_ex_data('/home/kacper/zajecia_inf/PythonProject/data/training_data')