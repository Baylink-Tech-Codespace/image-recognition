import face_recognition
import cv2
import os
import numpy as np
from encryptionProject.image_recognition.functions_and_constants import read_json
from encryptionProject.image_recognition.decrypt import decrypt


class SimpleFacerec:
    def __init__(self, Q):
        self.known_face_encodings = []
        self.known_face_names = []
        self.Q = Q
        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self):

        if os.path.exists('./data.json'):
            da = read_json('./data.json')
            self.known_face_names = list(da.keys())
            for i in list(da.values()):
                vectorized_function = np.vectorize(decrypt(self.Q))
                decoded_array = vectorized_function(np.array(i))
                self.known_face_encodings.append(decoded_array)
        else:
            print("No data present")
            exit(0)

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)        
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:         
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
