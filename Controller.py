import shutil
from Cropper import Cropper
from Extractor import Extractor
from Connections import Connections
from Classifier import Classifier
from Visualization import Visualization
from Settings import *

class Controller:
    def __init__(self):
        self.cropper = Cropper()
        self.extractor = Extractor(self.cropper)
        self.classifier = Classifier(self.extractor.images)
        self.connections = Connections(self.cropper, self.classifier)
        self.visualization = Visualization(self.connections)

    def load_connections_from_disk(self):
        self.connections.load_connections_from_disk()

    def generate_connections(self):
        self.clean_clusters_directory()
        self.clean_faces_directory()

        self.cropper.cropImagesInDirectory(DATA_PATH)
        self.extractor.extractFeaturesFromDirectory(FACES_PATH)
        self.extractor.fix_mapping_dictionary()
        self.classifier = Classifier(self.extractor.images)
        self.classifier.calculate_all_similarities()
        self.connections = Connections(self.cropper, self.classifier)
        self.connections.generate_connections()
        self.visualization = Visualization(self.connections)

    def get_results(self):
        return self.connections.get_clusters()

    def get_all_personal_pictures(self, clust_num):
        return self.visualization.get_all_personal_pictures(clust_num)

    def show_all_personal_pictures(self, clust_num):
        self.visualization.show_all_personal_pictures(clust_num)

    def draw_personal_graph(self, clust_num):
        self.visualization.draw_personal_graph(clust_num)

    def show_pictures_of_connection(self, clust_1, clust_2):
        self.visualization.show_pictures_of_connection(clust_1, clust_2)

    def get_pictures_of_connection(self, clust_1, clust_2):
        return self.visualization.get_pictures_of_connection(clust_1, clust_2)

    def clean_clusters_directory(self):
        for filename in os.listdir(CLUSTERS_PATH):
            file_path = os.path.join(CLUSTERS_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass

    def clean_faces_directory(self):
        for filename in os.listdir(FACES_PATH):
            file_path = os.path.join(FACES_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass