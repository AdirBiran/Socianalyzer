from Cropper import Cropper
from Extractor import Extractor
from Classifier3 import Classifier
from Settings import *
import os

def start():
    # create directories Data, Faces, Clusters:
    try:
        if not os.path.isdir('Data'):
            os.mkdir('Data')
        if not os.path.isdir('Faces'):
            os.mkdir('Faces')
        if not os.path.isdir('Clusters'):
            os.mkdir('Clusters')
    except OSError:
        print("Creation of the directories failed")

    cropper = Cropper()
    cropper.cropImagesInDirectory(DATA_PATH)

    extractor = Extractor()
    extractor.extractFeaturesFromDirectory(FACES_PATH)

    classifier = Classifier(extractor.images)
    classifier.calculate_all_similarities()

start()