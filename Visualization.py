"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
from Settings import *


class Visualization:
    def __init__(self, connections):
        self.connections = connections

    # First face of a cluster (represent of a cluster)
    def get_first_img_path_in_cluster(self, clust_num):
        face_name = self.connections.clustering_dictionary[str(clust_num)][0]
        return os.path.join(CLUSTERS_PATH, str(clust_num), face_name)

    # Shows all images belong to specific cluster
    def show_all_personal_pictures(self, clust_num):
        # Faces from cluster
        cluster_faces = self.connections.clustering_dictionary[str(clust_num)]
        paths = []

        # Looping each face
        for face in cluster_faces:
            # Get the image name from the inverse mapping dictionary
            img_name = self.connections.inverse_mapping_dictionary[face]
            img_path = os.path.join(DATA_PATH, img_name)
            paths.append(img_path)

        self.show_pictures(paths)

    # Show pictures of two clusters
    def show_pictures_of_connection(self, clust_num_1, clust_num_2):
        clust_num_1 = str(clust_num_1)
        clust_num_2 = str(clust_num_2)
        images = []

        # Looping all connections to get the relevant images
        for connection in self.connections.total_connections:
            if (connection[0] == clust_num_1 and connection[1] == clust_num_2) or (connection[0] == clust_num_2 and connection[1] == clust_num_1):
                images = connection[3]
                break

        # No common images
        if len(images) == 0:
            print("No common images found")
            return

        # Getting images' paths
        images_paths = [os.path.join(DATA_PATH, img) for img in images]

        self.show_pictures(images_paths)

    # Showing pictures
    def show_pictures(self, images_paths):

        # Resizing factore
        resize_factor = 0.5

        # Looping each image
        for img_path in images_paths:
            image = cv2.imread(img_path)

            # Getting sizes of image
            width = int(image.shape[1])
            height = int(image.shape[0])

            # Keep resizing while the image is larger than max sizes
            while width > IMAGE_MAX_WIDTH or height > IMAGE_MAX_HEIGHT:
                width = int(width * resize_factor)
                height = int(height * resize_factor)

            # Resized image dimensions
            dim = (width, height)

            # Resize image
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            # Show image
            cv2.imshow("", image)

            # Wait for key
            cv2.waitKey(0)

    # Draw all connections of specific cluster
    def draw_personal_graph(self, clust_num):
        # New graph
        G = nx.Graph()

        # Connections of clust_num
        other_connections = self.connections.get_connections(clust_num, sorted_by_connections=True)

        # Adding primary node of clust_num
        G.add_node(0, pos=(len(other_connections)/2, len(other_connections)))

        # Adding rest of nodes and edges
        i = 0
        for con in other_connections:
            G.add_node(int(con[0]), pos=(i, 0))
            G.add_edge(0, int(con[0]), weight=int(con[1]))
            i += 1

        # Drawing the graph
        pos = nx.get_node_attributes(G, 'pos')
        labels = nx.get_edge_attributes(G, 'weight')
        weights = nx.get_edge_attributes(G, 'weight').values()
        nx.draw(G, pos, width=list(weights))
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Parameters for printing the images
        ax = plt.gca()
        fig = plt.gcf()
        trans = ax.transData.transform
        trans2 = fig.transFigure.inverted().transform

        # Image size
        imsize = 0.1

        # Looping each node in the graph
        for n in G.nodes():

            # Base coordinates
            (x, y) = pos[n]

            # Figure coordinates
            xx, yy = trans((x, y))

            # Axes coordinates
            xa, ya = trans2((xx, yy))
            a = plt.axes([xa - imsize / 2.0, ya - imsize / 2.0, imsize, imsize])

            # Changing image based on cluster's number
            if n == 0:
                img = mpimg.imread(self.get_first_img_path_in_cluster(clust_num))
            else:
                img = mpimg.imread(self.get_first_img_path_in_cluster(n))

            # Showing the image over the node
            a.imshow(img)
            a.set_aspect('equal')
            a.axis('off')

        # Plotting the graph
        plt.show()
