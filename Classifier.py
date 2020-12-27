"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

from Settings import CLUSTERS_PATH, FACES_PATH, CLUSTERING_THRESHOLD
import numpy as np
from shutil import copyfile
import os
import shutil


class Classifier:
    def __init__(self, face_images_list):

        # List of the faces with encodings
        self.face_images_list = face_images_list

        # Cluster to faces
        self.clustering_dictionary = {}

        # Face to cluster
        self.inverse_clustering_dictionary = {}

        # Mean of clusters similarities
        self.mean_of_clusters = {}

        # Encodings (array of 128 numerical features)
        self.images_encodings = {}
        for image in face_images_list:
            self.images_encodings[image.name] = image.encoding

    # Set the list besides the constructor
    def set_face_images_list(self, face_images_list):
        self.face_images_list = face_images_list
        for image in face_images_list:
            self.images_encodings[image.name] = image.encoding

    # Similarity calculation between two faces
    def calculate_similarity(self, face_image_one, face_image_two):
        return np.dot(face_image_one, face_image_two) / (np.linalg.norm(face_image_one) * np.linalg.norm(face_image_two))

    # Calculate all similarities
    def cluster(self):
        i = 1

        # While there are faces to cluster
        while len(self.face_images_list) > 0:
            # Remove first image
            first_face_img = self.face_images_list[0]
            self.face_images_list.remove(first_face_img)

            cluster_path = os.path.join(CLUSTERS_PATH, str(i))
            is_clustered = False

            # For the rest of the images
            for compared_face_img in self.face_images_list:

                # Similarity calculation
                sim = self.calculate_similarity(compared_face_img.encoding, first_face_img.encoding)

                # Check threshold
                if sim > CLUSTERING_THRESHOLD:
                    is_clustered = True

                    # If cluster doesn't exist yet
                    if str(i) not in self.clustering_dictionary:
                        self.clustering_dictionary[str(i)] = [first_face_img.name]
                        self.inverse_clustering_dictionary[first_face_img.name] = str(i)

                    # If cluster's directory doesn't exist yet
                    if not os.path.isdir(cluster_path):
                        os.mkdir(cluster_path)
                        copyfile(os.path.join(FACES_PATH, first_face_img.name), os.path.join(CLUSTERS_PATH, str(i), first_face_img.name))

                    # Copy the face to the cluster
                    copyfile(os.path.join(FACES_PATH, compared_face_img.name), os.path.join(CLUSTERS_PATH, str(i), compared_face_img.name))

                    # Remove the face from the list
                    self.face_images_list.remove(compared_face_img)

                    # Set dictionaries
                    self.clustering_dictionary[str(i)].append(compared_face_img.name)
                    self.inverse_clustering_dictionary[compared_face_img.name] = str(i)

            # If no matching cluster found
            if not is_clustered:
                copyfile(os.path.join(FACES_PATH, first_face_img.name),
                         os.path.join(CLUSTERS_PATH, first_face_img.name))

            i += 1

        # after first loop try to unite close clusters
        all_dirs = [directory for directory in os.path.listdir(CLUSTERS_PATH) if os.path.isdir(os.path.join(CLUSTERS_PATH, directory))]
        self.recluster(all_dirs)

    # Cluster pairs of clusters based on similarity of cluster's means
    def recluster(self, files_list):
        self.calculate_clusters_means(files_list)
        for dir1 in files_list:
            for dir2 in files_list:
                if not dir1 == dir2:
                    sim = self.calculate_similarity(self.mean_of_clusters[dir1], self.mean_of_clusters[dir2])
                    if sim > 0.96:
                        self.unite_clusters(dir1,dir2)
                        self.calculate_clusters_means([directory for directory in os.path.listdir(CLUSTERS_PATH) if os.path.isdir(os.path.join(CLUSTERS_PATH, directory))])

    # Mean features for a cluster
    def get_mean_score_from_dir(self, directory_path):
        all_files = [file for file in os.path.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
        encodings = []
        for file in all_files:
            encodings.append(self.images_encodings[file])
        return np.mean(encodings, axis=0)

    # Unite two clusters
    def unite_clusters(self, dir1, dir2):
        if dir1 in self.clustering_dictionary.keys() and dir2 in self.clustering_dictionary.keys():
            self.clustering_dictionary[dir1].extend(self.clustering_dictionary[dir2])
            for image in self.clustering_dictionary[dir2]:
                self.inverse_clustering_dictionary[image] = dir1
                copyfile(os.path.join(FACES_PATH, image),
                         os.path.join(CLUSTERS_PATH + "//" + dir1, image))
            shutil.rmtree(CLUSTERS_PATH + "//" + dir2, ignore_errors=True)
            self.clustering_dictionary.pop(dir2)

    # Calculate the clusters means
    def calculate_clusters_means(self, all_files):
        for directory in all_files:
            mean = self.get_mean_score_from_dir(CLUSTERS_PATH + "\\" + directory)
            self.mean_of_clusters[directory] = mean
