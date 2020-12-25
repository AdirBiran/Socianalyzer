"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

from Settings import *
import numpy as np
from shutil import copyfile


class Classifier:
    def __init__(self, face_images_list):

        self.face_images_list = face_images_list
        self.clustering_dictionary = {}
        self.inverse_clustering_dictionary = {}

    # Similarity calculation between two faces
    def calculate_similarity(self, face_image_one, face_image_two):
        encoding_one = face_image_one.encoding
        encoding_two = face_image_two.encoding
        return np.dot(encoding_one, encoding_two) / (np.linalg.norm(encoding_one) * np.linalg.norm(encoding_two))

    # Calculate all similarities
    def calculate_all_similarities(self):
        i = 1
        while len(self.face_images_list) > 0:
            first_face_img = self.face_images_list[0]
            self.face_images_list.remove(first_face_img)
            cluster_path = os.path.join(CLUSTERS_PATH, str(i))

            is_clustered = False

            for compared_face_img in self.face_images_list:
                sim = self.calculate_similarity(compared_face_img, first_face_img)
                if sim > CLUSTERING_THRESHOLD:
                    is_clustered = True

                    if str(i) not in self.clustering_dictionary:
                        self.clustering_dictionary[str(i)] = [first_face_img.name]
                        self.inverse_clustering_dictionary[first_face_img.name] = str(i)
                    if not os.path.isdir(cluster_path):
                        os.mkdir(cluster_path)
                    copyfile(os.path.join(FACES_PATH, first_face_img.name), os.path.join(CLUSTERS_PATH, str(i), first_face_img.name))

                    copyfile(os.path.join(FACES_PATH, compared_face_img.name), os.path.join(CLUSTERS_PATH, str(i), compared_face_img.name))
                    self.face_images_list.remove(compared_face_img)
                    self.clustering_dictionary[str(i)].append(compared_face_img.name)
                    self.inverse_clustering_dictionary[compared_face_img.name] = str(i)

            if not is_clustered:
                copyfile(os.path.join(FACES_PATH, first_face_img.name),
                         os.path.join(CLUSTERS_PATH, first_face_img.name))

            i += 1
