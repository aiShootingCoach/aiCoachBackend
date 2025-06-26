import os
import cv2
import scanner
import json

def scan_ex_data(path):
    save_path = '/home/kacper/zajecia_inf/PythonProject/data/exemplary_data/'
    files = os.listdir(path)
    for file in files:
        file_path = path + '/' + file
        json_data = scanner.scan(file_path)
        save_file = save_path + file[:-4] + '.json'
        save_file = open(save_file, 'w')
        json_txt = json.dumps(json_data)
        save_file.write(json_txt)
        save_file.close()
    return 0

if __name__ == '__main__':
    scan_ex_data('/home/kacper/zajecia_inf/PythonProject/data/training_data')