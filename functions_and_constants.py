import json
import os
import cv2
from matplotlib import pyplot as plt
import numpy as np

from encryptionProject.image_recognition.face_detection import face_detect

E_D = 718281828459045
RSC_D = 145136923488338105028
cipher = {'00': '9', '01': '8', '02': '7', '03': '6', '04': '5', '05': '4', '06': '3', '07': '2', '08': '1', '09': '0',
          '10': 'a', '11': 'b', '12': 'c', '13': 'd', '14': 'e', '15': 'f', '16': 'g', '17': 'h', '18': 'i', '19': 'j',
          '20': 'k', '21': 'l', '22': 'm', '23': 'n', '24': 'o', '25': 'p', '26': 'q', '27': 'r', '28': 's', '29': 't',
          '30': 'u', '31': 'v', '32': 'w', '33': 'x', '34': 'y', '35': 'z', '36': 'A', '37': 'B', '38': 'C', '39': 'D',
          '40': 'E', '41': 'F', '42': 'G', '43': 'H', '44': 'I', '45': 'J', '46': 'K', '47': 'L', '48': 'M', '49': 'N',
          '50': 'O', '51': 'P', '52': 'Q', '53': 'R', '54': 'S', '55': 'T', '56': 'U', '57': 'V', '58': 'W', '59': 'X',
          '60': 'Y', '61': 'Z', '62': '`', '63': '~', '64': '!', '65': '@', '66': '#', '67': '$', '68': '%', '69': '^',
          '70': '&', '71': '*', '72': '(', '73': ')', '74': '-', '75': '_', '76': '+', '77': '=', '78': '[', '79': ']',
          '80': '{', '81': '}', '82': ';', '83': ':', '84': "'", '85': '"', '86': '\\', '87': '|', '88': ',', '89': '.',
          '90': '<', '91': '>', '92': '/', '93': '?', '94': '©', '95': '¥', '96': '£', '97': 'µ', '98': 'À', '99': 'È'}


def convert_to_six_digits(number):
    six_digit_number = number * 10 ** (6 - len(str(number)))
    return six_digit_number


def get_key(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None


def get_index(arr, ele):
    for i in range(len(arr)):
        if arr[i] == ele:
            return i
    return 0


def arr_to_int(arr):
    num_str = ''.join(map(str, arr))
    num_int = int(num_str)
    return num_int


def int_to_arr(num: int):
    if num < 0:
        num = num * -1
    num_str = str(int(num))
    num_array = [int(digit) for digit in num_str]
    return num_array


def calculate_G(x: int, const1: int, const2: int):
    res = (const1 * x) - const2
    if len(int_to_arr(res)) > 8:
        res = arr_to_int(int_to_arr(res)[:8])
    return res


def calculate_P(x: int):
    res = x ** 2 - x + 1
    if len(int_to_arr(res)) > 6:
        res = arr_to_int(int_to_arr(res)[:6])
    return convert_to_six_digits(res)


def group_integers(input_string, group_size=2):
    digits = [int(digit) for digit in str(input_string)]
    grouped_digits = [digits[i:i + group_size] for i in range(0, len(digits), group_size)]
    result = [int(''.join(map(str, group))) for group in grouped_digits]
    return result


def resize_video(width, height, max_width=600):
    if width > max_width:
        proportion = width / height
        video_width = max_width
        video_height = int(video_width / proportion)
    else:
        video_width = width
        video_height = height

    return video_width, video_height


def webcam(max_width=400, detect=True):
    decompress = None
    compress = None
    img_2 = None
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        image = frame.copy()
        if detect:
            if max_width is not None:
                video_width, video_height = resize_video(frame.shape[1], frame.shape[0], max_width)
                frame = cv2.resize(frame, (video_width, video_height))
                frame, img_2 = face_detect(frame)
        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    if detect:
        return image, frame, img_2
    else:
        return frame


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def write_data(file_path, name_, encodings):
    if os.path.exists(file_path):
        data = read_json(file_path)
    else:
        data = {}

    data.update({name_: encodings.tolist()})
    write_json(file_path, data)


def plot_arrays(arr, arr_name):
    x_values = np.arange(10)  # Assuming values from 0 to 9 on the x-axis

    # Plotting the single array on the graph with dynamic label
    plt.plot(x_values, arr, label=arr_name)

    # Adding labels and a legend
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()

    # Display the plot
    plt.show()
