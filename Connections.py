"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import json
from Settings import *

class Connections:
    def __init__(self, extractor, classifier):
        # Image to faces
        self.mapping_dictionary = extractor.mapping_dictionary
        # Face to image
        self.inverse_mapping_dictionary = extractor.inverse_mapping_dictionary
        # Cluster to faces
        self.clustering_dictionary = classifier.clustering_dictionary
        # Face to cluster
        self.inverse_clustering_dictionary = classifier.inverse_clustering_dictionary
        # All connections between clusters
        self.total_connections = []

        self.remove_duplicated_faces()

    def save_connections_to_disk(self):
        # Files
        mapping_dictionary_file = os.path.join(CONNECTIONS_PATH, 'mapping.json')
        inverse_mapping_dictionary_file = os.path.join(CONNECTIONS_PATH, 'inverse_mapping.json')
        clustering_dictionary_file = os.path.join(CONNECTIONS_PATH, 'clustering_mapping.json')
        inverse_clustering_file = os.path.join(CONNECTIONS_PATH, 'inverse_clustering_mapping.json')
        total_connections_file = os.path.join(CONNECTIONS_PATH, 'total_connections.json')

        # Mapping Dictionary
        with open(mapping_dictionary_file, 'w') as file:
            file.write(json.dumps(self.mapping_dictionary))

        # Inverse Mapping Dictionary
        with open(inverse_mapping_dictionary_file, 'w') as file:
            file.write(json.dumps(self.inverse_mapping_dictionary))

        # Clustering Dictionary
        with open(clustering_dictionary_file, 'w') as file:
            file.write(json.dumps(self.clustering_dictionary))

        # Inverse Clustering Dictionary
        with open(inverse_clustering_file, 'w') as file:
            file.write(json.dumps(self.inverse_clustering_dictionary))

        # Total Connections
        with open(total_connections_file, 'w') as file:
            file.write(json.dumps(self.total_connections))

    def load_connections_from_disk(self):
        # Files
        mapping_dictionary_file = os.path.join(CONNECTIONS_PATH, 'mapping.json')
        inverse_mapping_dictionary_file = os.path.join(CONNECTIONS_PATH, 'inverse_mapping.json')
        clustering_dictionary_file = os.path.join(CONNECTIONS_PATH, 'clustering_mapping.json')
        inverse_clustering_file = os.path.join(CONNECTIONS_PATH, 'inverse_clustering_mapping.json')
        total_connections_file = os.path.join(CONNECTIONS_PATH, 'total_connections.json')

        # Mapping Dictionary
        with open(mapping_dictionary_file, 'r') as file:
            self.mapping_dictionary = json.loads(file.read())

        # Inverse Mapping Dictionary
        with open(inverse_mapping_dictionary_file, 'r') as file:
            self.inverse_mapping_dictionary = json.loads(file.read())

        # Clustering Dictionary
        with open(clustering_dictionary_file, 'r') as file:
            self.clustering_dictionary = json.loads(file.read())

        # Inverse Clustering Dictionary
        with open(inverse_mapping_dictionary_file, 'r') as file:
            self.inverse_clustering_dictionary = json.loads(file.read())

        # Total Connections
        with open(total_connections_file, 'r') as file:
            self.total_connections = json.loads(file.read())

    # Other faces in the same image of the "face" object
    def get_other_faces_in_same_image(self, face):
        whole_image = self.inverse_mapping_dictionary[face]
        # Slicing for new list (deep copy)
        res = self.mapping_dictionary[whole_image][:]

        # Remove the current face from results
        res.remove(face)

        return res

    # All faces in the same image of the "face" object
    def get_all_faces_in_same_image(self, face):
        whole_image = self.inverse_mapping_dictionary[face]
        # Slicing for new list (deep copy)
        res = self.mapping_dictionary[whole_image][:]

        return res

    # Get all faces for each cluster
    def get_all_clusters_faces(self):
        return [self.clustering_dictionary[cl_faces] for cl_faces in self.clustering_dictionary]

    # Whole image from face
    def get_image_from_face(self, face):
        return self.inverse_mapping_dictionary[face]

    # All faces in image
    def get_faces_from_image(self, image):
        return self.mapping_dictionary[image][:]

    # True if both faces in same image, False otherwise
    def are_faces_in_same_image(self, face_1, face_2):
        return self.inverse_mapping_dictionary[face_1] == self.inverse_mapping_dictionary[face_2]

    # Get all faces in the same cluster of "face" object
    def get_all_faces_in_cluster(self, face):
        for clust in self.clustering_dictionary:
            if face in self.clustering_dictionary[clust]:
                return self.clustering_dictionary[clust][:]

    def generate_connections(self):
        generated_connections = []

        # Looping through all combinations of clusters
        for cluster in self.clustering_dictionary:
            for other_cluster in self.clustering_dictionary:
                if cluster != other_cluster:
                    # Looping through all combinations of faces between 2 clusters
                    for face_1 in self.clustering_dictionary[cluster]:
                        for face_2 in self.clustering_dictionary[other_cluster]:
                            if self.are_faces_in_same_image(face_1, face_2):
                                rec = [cluster, other_cluster, 1, [self.get_image_from_face(face_1)]]
                                generated_connections.append(rec)

        # List of all clusters
        clusters_list = [cl for cl in self.clustering_dictionary]

        # Looping through all combinations of clusters
        for i in range(len(clusters_list)):
            for j in range(i+1, len(clusters_list)):
                cl = clusters_list[i]
                cl_2 = clusters_list[j]
                if cl != cl_2:
                    # Grouping connections related to same clusters
                    group_con = [con for con in generated_connections if con[0] == cl and con[1] == cl_2]
                    # Aggregating connections related to same clusters
                    fixed_con = self.group_connections(group_con)
                    if len(fixed_con) > 0:
                        self.total_connections.append(fixed_con)

        # Saving connections to disk after generating
        self.save_connections_to_disk()

    # Group connections related to same clusters
    def group_connections(self, group_con):
        res = []
        if len(group_con) > 0:
            # [cluster_1, cluster_2, num_of_connections, list_of_common_images]
            res = [group_con[0][0], group_con[0][1], len(group_con), []]
            for con in group_con:
                # If image is not already exist
                if con[3][0] not in res[3]:
                    res[3].append(con[3][0])
        return res

    # Connections of specific cluster
    def get_connections(self, cluster_num, sorted_by_connections=False):
        cluster_num = str(cluster_num)

        # Cluster is the first cell ("connect with")
        results = [con[1:] for con in self.total_connections if con[0] == cluster_num]
        # Cluster is the second cell ("being connected to")
        second_cell_clusters = [con for con in self.total_connections if con[1] == cluster_num]

        # Unite results
        row = []
        for rec in second_cell_clusters:
            row.append(rec[0])
            row.append(rec[2])
            row.append(rec[3])
            results.append(row)
            row = []

        # Sorting
        if sorted_by_connections:
            results.sort(key = lambda x: x[1], reverse=True)

        return results

    # Removing duplicate faces
    def remove_duplicated_faces(self):
        # All clusters with all faces
        clusters_faces = self.get_all_clusters_faces()

        # Looping each cluster
        for cluster in clusters_faces:

            # Looping each pair of faces
            for face_1 in cluster:
                for face_2 in cluster:
                    if face_1 is not face_2:
                        # If two faces in same cluster belong to same image
                        if self.are_faces_in_same_image(face_1, face_2):
                            img = self.inverse_mapping_dictionary[face_2]

                            # Remove from mapping dictionary
                            self.mapping_dictionary[img].remove(face_2)

                            # Remove from inverse mapping dictionary
                            self.inverse_mapping_dictionary.pop(face_2)
                            clust = self.inverse_clustering_dictionary[face_2]

                            # Remove from clustering dictionary
                            self.clustering_dictionary[clust].remove(face_2)

                            # Remove from inverse clustering dictionary
                            self.inverse_clustering_dictionary.pop(face_2)

                            # Remove file
                            os.remove(os.path.join(CLUSTERS_PATH, clust, face_2))
