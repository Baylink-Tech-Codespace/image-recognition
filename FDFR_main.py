from encryptionProject.image_recognition.P_x_G_x import generate_P_G_Q
from encryptionProject.image_recognition.functions_and_constants import webcam, write_data, plot_arrays
import cv2
import os
from encryptionProject.image_recognition.encrypt import encrypt
from encryptionProject.image_recognition.face_encodings import face_encoding
from encryptionProject.image_recognition.face_detection import face_detect
import numpy as np

from encryptionProject.image_recognition.simple_facerec import SimpleFacerec


class Face_Data:
    def __init__(self, sender="216.3.128.12", receiver="192.1.168.43"):
        self.sender = sender
        self.receiver = receiver
        self.G, self.P, self.Q = generate_P_G_Q(self.sender, self.receiver)
        self.file_path = './data.json'

    def encode(self):
        diff = int(input("Webcam?:-"))
        vectorized_function = np.vectorize(encrypt(self.Q))
        if diff:
            name = input("Enter Name:-")
            image2, pf2, img_2 = webcam(800)
            encodings = face_encoding(image2)
            encrypted = vectorized_function(np.array(encodings))
            write_data(self.file_path, name, encrypted[0])
        else:
            path = input("Enter image directory path:-")
            if not os.path.exists(path):
                print("Incorrect path please try again")
                exit(0)
            for i in os.listdir(path):
                try:
                    print("Encoding:-", i)
                    image = cv2.imread(f'{path}/{i}')
                    image2, img_2 = face_detect(image)
                    encodings = face_encoding(image2)
                    name = i.split('.')[0]
                    encrypted = vectorized_function(encodings)
                    write_data(self.file_path, name, encrypted[0])
                except Exception:
                    raise Exception
        print("Image encoded successfully")

    def detect(self):
        sfr = SimpleFacerec(self.Q)
        sfr.load_encoding_images()
        diff = int(input("Webcam?"))
        if diff:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                face_locations, face_names = sfr.detect_known_faces(frame)
                for face_loc, name in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1)
                if key == 27 or cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            path = input("Enter image directory path:-")
            if not os.path.exists(path):
                print("Incorrect path please try again")
                exit(0)
            for i in os.listdir(path):

                image = cv2.imread(f'{path}/{i}')
                face_locations, face_names = sfr.detect_known_faces(image)
                for face_loc, name in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                    cv2.putText(image, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 200), 2)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 200), 2)
                cv2.imshow(i, image)
                key = cv2.waitKey(0)


if __name__ == "__main__":
    s = input("Enter Sender:-")
    r = input("Enter Receiver:-")
    fd = Face_Data(sender=s,receiver=r)
    choice = int(input("1. Encode\n2. Detect\n3.Plot P,Q,G\n5.Exit\nChoose:-"))
    while choice != 5:
        if choice == 1:
            fd.encode()
        elif choice == 2:
            fd.detect()
        elif choice == 3:
            abs_G = []
            for i in fd.G:
                abs_G.append(abs(i))
            plot_arrays(fd.P, "P(x)")
            plot_arrays(fd.G, "(G(x)")
            plot_arrays(fd.Q, "Q(x)")
        else:
            print("Invalid choice")
        choice = int(input("1. Encode\n2. Detect\n3.Plot P,Q,G\n5.Exit\nChoose:-"))
