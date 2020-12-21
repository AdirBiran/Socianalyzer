from Extractor import Extractor
from Settings import *
import numpy as np
from shutil import copyfile
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd


class Classifier:
    def __init__(self, face_images_list):
        self.face_images_list = face_images_list
        self.face_images_encoded_list = []
        for face_image in face_images_list:
            self.face_images_encoded_list.append(face_image.encoding)

    def calculate_all_similarities(self):
        # Fitting K-Means to the dataset
        dataset1 =pd.DataFrame()
        dataset1['Image'] = self.face_images_list
        # find out how to estimate number of clusters
        kmeans = KMeans(n_clusters=18, init='k-means++', random_state=42)
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

