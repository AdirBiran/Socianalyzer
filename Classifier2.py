from Extractor import Extractor
from Settings import *
import numpy as np
from shutil import copyfile


ext = Extractor()
dirPath = FACES_PATH
ext.extractFeaturesFromDirectory(dirPath)


class Classifier:
    def __init__(self, face_images_list):
        self.face_images_list = face_images_list

    def calculate_similarity(self, face_image_one, face_image_two):
        encoding_one = face_image_one.encoding
        encoding_two = face_image_two.encoding
        return np.dot(encoding_one, encoding_two) / (np.linalg.norm(encoding_one) * np.linalg.norm(encoding_two))

    def calculate_all_similarities(self):
        i = 1
        while len(self.face_images_list) > 0:
            first_face_img = self.face_images_list[0]
            self.face_images_list.remove(first_face_img)
            cluster_path = os.path.join(CLUSTERS_PATH, str(i))
            os.mkdir(cluster_path)
            copyfile(os.path.join(FACES_PATH, first_face_img.name), os.path.join(CLUSTERS_PATH, str(i), first_face_img.name))

            for compared_face_img in self.face_images_list:
                sim = self.calculate_similarity(compared_face_img, first_face_img)
                if sim > CLUSTERING_THRESHOLD:
                    copyfile(os.path.join(FACES_PATH, compared_face_img.name), os.path.join(CLUSTERS_PATH, str(i), compared_face_img.name))
                    self.face_images_list.remove(compared_face_img)

            i += 1