"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import shutil
from Cropper import Cropper
from Extractor import Extractor
from Connections import Connections
from Classifier import Classifier
from Visualization import Visualization
import os
from Settings import FACES_PATH, CLUSTERS_PATH, DATA_PATH


class Controller:
    def __init__(self):

        # Init basic objects
        self.cropper = Cropper()
        self.extractor = Extractor(self.cropper)
        self.classifier = Classifier(self.extractor.images)
        self.connections = Connections(self.extractor, self.classifier)
        self.visualization = Visualization(self.connections)

    # Load connections from the disk
    def load_connections_from_disk(self):
        self.connections.load_connections_from_disk()

    # Generate connections
    def generate_connections(self):

        # Clean faces and clusters directory
        self.clean_clusters_directory()
        self.clean_faces_directory()

        # Crop faces
        self.cropper.crop_images_in_directory(DATA_PATH)

        # Extract features for each face
        self.extractor.extract_features_from_directory(FACES_PATH)

        # Remove images that do not represent a face (remove false positives)
        self.extractor.fix_mapping_dictionary()

        # Set the cropper images
        self.classifier.set_face_images_list(self.extractor.images)

        # Cluster the faces
        self.classifier.cluster()

        # Set the extractor and classifier after the clustering
        self.connections.set_extractor_classifier(self.extractor, self.classifier)

        # Remove duplicate faces (remove false positives)
        self.connections.remove_duplicated_faces()

        # Generate the connections
        self.connections.generate_connections()

        # Set connections for the visualization object
        self.visualization.set_connections(self.connections)

    # Get clusters
    def get_results(self):
        return self.connections.get_clusters()

    # Get all personal pictures
    def get_all_personal_pictures(self, clust_num):
        return self.visualization.get_all_personal_pictures(clust_num)

    # Draw personal connections graph
    def draw_personal_graph(self, clust_num):
        self.visualization.draw_personal_graph(clust_num)

    # Get the connection's pictures
    def get_pictures_of_connection(self, cluster_1, cluster_2):
        return self.visualization.get_pictures_of_connection(cluster_1, cluster_2)

    # Clean clusters directory
    def clean_clusters_directory(self):
        for filename in os.listdir(CLUSTERS_PATH):
            file_path = os.path.join(CLUSTERS_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                pass

    # Clean faces directory
    def clean_faces_directory(self):
        for filename in os.listdir(FACES_PATH):
            file_path = os.path.join(FACES_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                pass

    # Count directories
    def count_directories(self, path):
        return len([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])

    # Count files
    def count_files(self, path):
        return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
