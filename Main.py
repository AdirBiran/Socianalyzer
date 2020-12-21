import shutil

from Cropper import Cropper
from Extractor import Extractor
from Classifier2 import Classifier
from Connections import Connections
from Settings import *
import os

def clean_clusters():
    for filename in os.listdir(CLUSTERS_PATH):
        file_path = os.path.join(CLUSTERS_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            pass

def clean_faces():
    for filename in os.listdir(FACES_PATH):
        file_path = os.path.join(FACES_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            pass

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

    clean_faces()
    clean_clusters()

    cropper = Cropper()
    cropper.cropImagesInDirectory(DATA_PATH)

    extractor = Extractor(cropper)
    extractor.extractFeaturesFromDirectory(FACES_PATH)
    extractor.fix_mapping_dictionary()

    classifier = Classifier(extractor.images)
    classifier.calculate_all_similarities()

    connections = Connections(extractor, classifier)
    connections.generate_connections()






start()