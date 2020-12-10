from imutils import paths
import face_recognition
import cv2
from Settings import *
from FaceImage import FaceImage

class Extractor:

    def __init__(self):
        self.images = []

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