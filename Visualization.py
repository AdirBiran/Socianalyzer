"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import ctypes

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
import os
from Settings import CLUSTERS_PATH, DATA_PATH


class Visualization:
    def __init__(self, connections):
        self.connections = connections

    # Set the connections object besides the constructor
    def set_connections(self, connections):
        self.connections = connections

    # First face of a cluster (represent of a cluster)
    def get_first_img_path_in_cluster(self, cluster_num):
        face_name = self.connections.clustering_dictionary[str(cluster_num)][0]
        return os.path.join(CLUSTERS_PATH, str(cluster_num), face_name)

    def get_all_personal_pictures(self, cluster_num):

        # Faces from cluster
        cluster_faces = self.connections.clustering_dictionary[str(cluster_num)]

        paths = []

        # Looping each face
        for face in cluster_faces:
            # Get the image name from the inverse mapping dictionary
            img_name = self.connections.inverse_mapping_dictionary[face]
            img_path = os.path.join(DATA_PATH, img_name)
            paths.append(img_path)

        return paths

    def get_pictures_of_connection(self, cluster_num_1, cluster_num_2):
        cluster_num_1 = str(cluster_num_1)
        cluster_num_2 = str(cluster_num_2)
        images = []

        # Looping all connections to get the relevant images
        for connection in self.connections.total_connections:
            if (connection[0] == cluster_num_1 and connection[1] == cluster_num_2) or (
                    connection[0] == cluster_num_2 and connection[1] == cluster_num_1):
                images = connection[3]
                break

        # No common images
        if len(images) == 0:
            return

        # Getting images' paths
        images_paths = [os.path.join(DATA_PATH, img) for img in images]

        return images_paths

    # Draw all connections of specific cluster
    def draw_personal_graph(self, cluster_num):
        # New graph
        graph = nx.Graph()

        # Connections of cluster_num
        other_connections = self.connections.get_connections(cluster_num, sorted_by_connections=True)

        # No connections found
        if len(other_connections) == 0:
            ctypes.windll.user32.MessageBoxW(0, "No connections found :(", "Error!", 0)
            return

        # Adding primary node of cluster_num
        graph.add_node(0, pos=(len(other_connections)/2, len(other_connections)))

        # Adding rest of nodes and edges
        i = 0
        for con in other_connections:
            graph.add_node(int(con[0]), pos=(i, 0))
            graph.add_edge(0, int(con[0]), weight=int(con[1]))
            i += 1

        # Drawing the graph
        pos = nx.get_node_attributes(graph, 'pos')
        labels = nx.get_edge_attributes(graph, 'weight')
        weights = nx.get_edge_attributes(graph, 'weight').values()
        nx.draw(graph, pos, width=list(weights))
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        # Parameters for printing the images
        ax = plt.gca()
        fig = plt.gcf()
        trans = ax.transData.transform
        trans2 = fig.transFigure.inverted().transform

        # Image size
        img_size = 0.1

        # Looping each node in the graph
        for n in graph.nodes():

            # Base coordinates
            (x, y) = pos[n]

            # Figure coordinates
            xx, yy = trans((x, y))

            # Axes coordinates
            xa, ya = trans2((xx, yy))
            a = plt.axes([xa - img_size / 2.0, ya - img_size / 2.0, img_size, img_size])

            # Changing image based on cluster's number
            if n == 0:
                img = mpimg.imread(self.get_first_img_path_in_cluster(cluster_num))
            else:
                img = mpimg.imread(self.get_first_img_path_in_cluster(n))

            # Showing the image over the node
            a.imshow(img)
            a.set_aspect('equal')
            a.axis('off')

        # Full screen
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')

        # Plotting the graph
        plt.show()
