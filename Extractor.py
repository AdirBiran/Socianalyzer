"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

from imutils import paths
import face_recognition
import cv2
import os
from FaceImage import FaceImage


class Extractor:

    def __init__(self, cropper):
        self.images = []
        # Image to faces (String, List)
        self.mapping_dictionary = cropper.mapping_dictionary
        # Face to image (String, String)
        self.inverse_mapping_dictionary = cropper.inverse_mapping_dictionary

    # Extract features from a face image
    def extract_features_from_face_image(self, image_path):
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Getting the face encodings
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)

        # If picture is a face
        if len(encodings) > 0:
            return encodings[0]
        else:
            os.remove(image_path)
            return None

    # Extract features from a directory
    def extract_features_from_directory(self, dir_path):
        # All images in directory
        images_paths = list(paths.list_images(dir_path))

        for path in images_paths:
            face_name = path[path.rfind("\\") + 1:]
            face_encoding = self.extract_features_from_face_image(path)
            if face_encoding is not None:
                face_image_obj = FaceImage(face_name, face_encoding)
                self.images.append(face_image_obj)

    # Remove "unfaces" images from the mapping dictionary
    def fix_mapping_dictionary(self):
        # Just faces (without noise images)
        faces_names = [f.name for f in self.images]

        # New mappings
        new_mapping = {}
        new_inverse_mapping = {}

        # Saves only faces in mapping
        for key in self.mapping_dictionary:
            new_mapping[key] = []
            for face in self.mapping_dictionary[key]:
                if face in faces_names:
                    new_mapping[key].append(face)

        # Saves only faces in inverse mapping
        for face in self.inverse_mapping_dictionary:
            if face in faces_names:
                new_inverse_mapping[face] = self.inverse_mapping_dictionary[face]

        # Save new mappings
        self.mapping_dictionary = new_mapping
        self.inverse_mapping_dictionary = new_inverse_mapping
