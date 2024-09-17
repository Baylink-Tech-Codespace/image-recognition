import cv2
from face_recognition import face_locations


# image = cv2.imread("profile.jpg")
def face_detect(image,write=False):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_location = face_locations(image_gray)
    img_2 = None
    # Draw bounding boxes on the image
    for coordinates in face_location:
        y1, x2, y2, x1 = coordinates
        img_2 = image_gray[x1:x2, y1:y2]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 200), 4)
    # Save the detected faces
    if write:
        cv2.imwrite("detected.png", image)
    return image, img_2
