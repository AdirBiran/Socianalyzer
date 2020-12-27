"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import cv2
import os
from Settings import RESOURCES_PATH, FACES_PATH


class Cropper:
    def __init__(self, min_size=50):
        self.cascPath = os.path.join(RESOURCES_PATH, 'haarcascade_frontalface_default.xml')
        self.faceCounter = 1
        self.min_size = min_size
        # Image to faces (String, List)
        self.mapping_dictionary = {}
        # Face to image (String, String)
        self.inverse_mapping_dictionary = {}

    # imagePath = absolute path to image
    def crop_image(self, image_path):
        face_cascade = cv2.CascadeClassifier(self.cascPath)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Image name
        whole_image_name = image_path[image_path.rfind("/") + 1:]

        self.mapping_dictionary[whole_image_name] = []

        # Algorithm's parameters
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=9,
            minSize=(self.min_size, self.min_size),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        faces_found = 0

        # Foreach face found in the image
        for (x, y, w, h) in faces:
            cropped_face = image[y:y + h, x:x + w]

            # Saving to mappings
            face_name = "face" + str(self.faceCounter) + ".jpg"
            self.mapping_dictionary[whole_image_name].append(face_name)
            self.inverse_mapping_dictionary[face_name] = whole_image_name

            # Save face image
            face_path = FACES_PATH + "/" + face_name
            cv2.imwrite(face_path, cropped_face)
            self.faceCounter += 1
            faces_found += 1

    # dir_path = absolute path to directory
    def crop_images_in_directory(self, dir_path):
        images_paths_to_crop = []
        for file in os.listdir(dir_path):
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                images_paths_to_crop.append(os.path.join(dir_path, file).replace("\\", "/"))

        for img_path in images_paths_to_crop:
            self.crop_image(img_path)
