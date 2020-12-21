
class Connections:
    def __init__(self, extractor, classifier):
        # Image to faces
        self.mapping_dictionary = extractor.mapping_dictionary
        # Face to image
        self.inverse_mapping_dictionary = extractor.inverse_mapping_dictionary
        # Cluster to faces
        self.clustering_dictionary = classifier.clustering_dictionary

        self.connections = []

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
        for cluster in self.clustering_dictionary:
            for other_cluster in self.clustering_dictionary:
                if cluster != other_cluster:
                    for face_1 in self.clustering_dictionary[cluster]:
                        for face_2 in self.clustering_dictionary[other_cluster]:
                            if self.are_faces_in_same_image(face_1, face_2):
                                rec = [cluster, other_cluster, 1, [self.get_image_from_face(face_1)]]
                                generated_connections.append(rec)

        clusters_list = [cl for cl in self.clustering_dictionary]

        for i in range(len(clusters_list)):
            for j in range(i+1, len(clusters_list)):
                cl = clusters_list[i]
                cl_2 = clusters_list[j]
                if cl != cl_2:
                    group_con = [con for con in generated_connections if con[0] == cl and con[1] == cl_2]
                    fixed_con = self.group_connections(group_con)
                    if len(fixed_con) > 0:
                        self.connections.append(fixed_con)

    def group_connections(self, group_con):
        res = []
        if len(group_con) > 0:
            res = [group_con[0][0], group_con[0][1], len(group_con), []]
            for con in group_con:
                if con[3][0] not in res[3]:
                    res[3].append(con[3][0])
        return res
