from encryptionProject.image_recognition.P_x_G_x import generate_P_G_Q
from encryptionProject.image_recognition.face_detection import face_detect
from encryptionProject.image_recognition.functions_and_constants import int_to_arr, arr_to_int, group_integers, webcam,write_data,cipher
from encryptionProject.image_recognition.face_encodings import face_encoding
import numpy as np
import os
import cv2


def encrypt(Q):
    def encrypt_np(encoding):
        m_encod = encoding*1e6
        neg = False
        if m_encod < 0:
            neg = True
        e_arr = int_to_arr(abs(m_encod))
        res = []
        for j in range(len(e_arr)):
            res.append(Q[e_arr[j]] + j)
        et = str(arr_to_int(res))
        arr = group_integers(et)
        cipher_text = ""
        for j in arr:
            if j<10:
                key = f'0{j}'
            else:
                key = str(j)
            cipher_text += cipher[key]
        if neg:
            return "-" + cipher_text
        return cipher_text
    return encrypt_np


if __name__ == "__main__":
    sender = "216.3.128.12"
    receiver = "192.1.168.43"
    file_path = "./data.json"


