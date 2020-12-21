from imutils import paths
import face_recognition
import cv2
from Settings import *
from FaceImage import FaceImage

class Extractor:

    def __init__(self, cropper):
        self.images = []
        # Image to faces (String, List)
        self.mapping_dictionary = cropper.mapping_dictionary
        # Face to image (String, String)
        self.inverse_mapping_dictionary = cropper.inverse_mapping_dictionary

    def extractFeaturesFromFaceImage(self, imagePath):
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        if len(encodings) > 0:
            return encodings[0]
        else:
            os.remove(imagePath)
            return None

    def extractFeaturesFromDirectory(self, dirPath):
        imagePaths = list(paths.list_images(dirPath))
        for path in imagePaths:
            face_name = path[path.rfind("\\") + 1:]
            face_encoding = self.extractFeaturesFromFaceImage(path)
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