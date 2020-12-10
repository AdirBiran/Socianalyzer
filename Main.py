from Cropper import Cropper
from Extractor import Extractor
from Classifier2 import Classifier
from Settings import *

def start():
    cropper = Cropper()
    cropper.cropImagesInDirectory(DATA_PATH)

    extractor = Extractor()
    extractor.extractFeaturesFromDirectory(FACES_PATH)

    classifier = Classifier(extractor.images)
    classifier.calculate_all_similarities()

start()