import cv2
import numpy as np
from face_recognition import face_encodings


def face_encoding(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    np.set_printoptions(formatter={'float_kind': '{:f}'.format})
    encodings = np.array(face_encodings(image_rgb))
    return encodings
