"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import shutil

from Cropper import Cropper
from Extractor import Extractor
from Classifier2 import Classifier
from Connections import Connections
from Visualization import Visualization
from Settings import *
import os
"""

Checklist:
Change functions to static wherever possible
Comments on all functions
Unneeded imports
Change class FaceImage? maybe not needed
Try improve clustering by higher threshold and recluster

"""

def clean_clusters_directory():
    for filename in os.listdir(CLUSTERS_PATH):
        file_path = os.path.join(CLUSTERS_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            pass


def clean_faces_directory():
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

    load_data_from_disk()


def load_data_from_disk():
    # clean_faces_directory()
    # clean_clusters_directory()

    cropper = Cropper()

    extractor = Extractor(cropper)
    classifier = Classifier(extractor.images)
    connections = Connections(extractor, classifier)

    connections.load_connections_from_disk()

    visualize = Visualization(connections)
    # visualize.draw_personal_graph(99)
    # visualize.show_all_personal_pictures(99)
    # visualize.show_pictures_of_connection(99, 34)


def prepare_data():
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
