"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

from Settings import *
import numpy as np
from shutil import copyfile
from os import listdir
from os.path import isfile, join, isdir
import shutil


class Classifier:
    def __init__(self, face_images_list):

        self.face_images_list = face_images_list
        self.clustering_dictionary = {}
        self.inverse_clustering_dictionary = {}
        self.mean_of_clusters = {}
        self.images_encodings = {}
        for image in face_images_list:
            self.images_encodings[image.name] = image.encoding

    # Similarity calculation between two faces
    def calculate_similarity(self, face_image_one, face_image_two):
        # encoding_one = face_image_one.encoding
        # encoding_two = face_image_two.encoding
        return np.dot(face_image_one, face_image_two) / (np.linalg.norm(face_image_one) * np.linalg.norm(face_image_two))

    # Calculate all similarities
    def calculate_all_similarities(self):
        i = 1
        while len(self.face_images_list) > 0:
            first_face_img = self.face_images_list[0]
            self.face_images_list.remove(first_face_img)
            cluster_path = os.path.join(CLUSTERS_PATH, str(i))

            is_clustered = False

            for compared_face_img in self.face_images_list:
                sim = self.calculate_similarity(compared_face_img.encoding, first_face_img.encoding)
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
        # after first loop try to unite close clusters
        all_dirs = [dir for dir in listdir(CLUSTERS_PATH) if isdir(join(CLUSTERS_PATH, dir))]
        self.reculster(all_dirs)



    def recluster(self, files_list):
        self.calculate_clusters_means(files_list)
        for dir1 in files_list:
            for dir2 in files_list:
                if not dir1 == dir2:
                    sim = self.calculate_similarity(self.mean_of_clusters[dir1], self.mean_of_clusters[dir2])
                    if sim > 0.96:
                        self.unite_clusters(dir1,dir2)
                        self.calculate_clusters_means([dir for dir in listdir(CLUSTERS_PATH) if isdir(join(CLUSTERS_PATH, dir))])

    def get_mean_score_from_dir(self, directory_path):
        all_files = [file for file in listdir(directory_path) if isfile(join(directory_path, file))]
        encodings = []
        for file in all_files:
            encodings.append(self.images_encodings[file])
        return np.mean(encodings, axis=0)

    def unite_clusters(self, dir1, dir2):
        if dir1 in self.clustering_dictionary.keys() and dir2 in self.clustering_dictionary.keys():
            self.clustering_dictionary[dir1].extend(self.clustering_dictionary[dir2])
            for image in self.clustering_dictionary[dir2]:
                self.inverse_clustering_dictionary[image] = dir1
                copyfile(os.path.join(FACES_PATH, image),
                         os.path.join(CLUSTERS_PATH + "//" + dir1, image))
            shutil.rmtree(CLUSTERS_PATH + "//" + dir2, ignore_errors=True)
            self.clustering_dictionary.pop(dir2)

    def calculate_clusters_means(self,all_files):
        for dir in all_files:
            mean = self.get_mean_score_from_dir(CLUSTERS_PATH + "\\" + dir)
            self.mean_of_clusters[dir] = mean