"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

from Settings import *
from shutil import copyfile
from sklearn.cluster import KMeans
import scipy.spatial.distance as sdist
import matplotlib.pyplot as plt
from scipy.spatial import distance

import pandas as pd


class Classifier:
    def __init__(self, face_images_list):
        self.face_images_list = face_images_list
        self.face_images_encoded_list = []
        for face_image in face_images_list:
            self.face_images_encoded_list.append(face_image.encoding)


    def run_KMeans_in_loop(self):
        history = {}
        for i in range(1,len(self.face_images_list),3):
            kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
            y_kmeans = kmeans.fit_predict(self.face_images_encoded_list)
            #y_kmeans1 = y_kmeans + 1
            history[kmeans] = y_kmeans
        return history

    def get_distances_from_centers(self, history):
        distances_from_centers = pd.DataFrame(columns=['K','Score'])
        k = []
        scores = []
        for kmeans in history.keys():
            dist = []
            centroids = kmeans.cluster_centers_
            clusters = history[kmeans]
            # find a different system to calculate distance
            for j in range(len(self.face_images_encoded_list)):
                dist.append(distance.euclidean(self.face_images_encoded_list[j], centroids[clusters][j]))
            k.append(kmeans.n_clusters)
            scores.append(sum(dist)/len(dist))

        distances_from_centers['K'] = k
        distances_from_centers['Score'] = scores
        return distances_from_centers

    def calculate_all_similarities(self):
        # Fitting K-Means to the dataset
        dataset1 =pd.DataFrame()
        dataset1['Image'] = self.face_images_list
        history = self.run_KMeans_in_loop()
        distances_from_centers = self.get_distances_from_centers(history)
        # print(distances_from_centers)
        plt.plot('K','Score',data=distances_from_centers)
        plt.show()
        k = self.find_optimal_k(distances_from_centers)
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
        y_kmeans = kmeans.fit_predict(self.face_images_encoded_list)
        # beginning of  the cluster numbering with 1 instead of 0
        y_kmeans1 = y_kmeans + 1
        # New Dataframe called cluster
        # cluster = pd.DataFrame(y_kmeans1)
        # Adding cluster to the Dataset1
        dataset1['cluster'] = y_kmeans1
        for index, row in dataset1.iterrows():
            # save image in directory of cluster's number
            cluster_path = os.path.join(CLUSTERS_PATH, str(row['cluster']))
            if not os.path.isdir(cluster_path):
                os.mkdir(cluster_path)
            copyfile(os.path.join(FACES_PATH, row['Image'].name),
                     os.path.join(CLUSTERS_PATH, str(row['cluster']), row['Image'].name))

    def find_optimal_k(self, distances_from_centers):
        min_value = distances_from_centers['Score'].idxmin()
        return distances_from_centers['K'][min_value]


