"""
Authors:
    Liat Cohen  205595283
    Adir Biran  308567239
    12/2020
"""

import cv2
from Settings import *


class Cropper:
    def __init__(self, min_size=45):
        self.cascPath = os.path.join(RESOURCES_PATH, 'haarcascade_frontalface_default.xml')
        self.faceCounter = 1
        self.min_size = min_size
        # Image to faces (String, List)
        self.mapping_dictionary = {}
        # Face to image (String, String)
        self.inverse_mapping_dictionary = {}

    #imagePath = absolute path to image
    def cropImage(self, imagePath):
        faceCascade = cv2.CascadeClassifier(self.cascPath)
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Image name
        whole_image_name = imagePath[imagePath.rfind("/") + 1:]

        self.mapping_dictionary[whole_image_name] = []

        # Algorithm's parameters
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.007,
            minNeighbors=9,
            minSize=(self.min_size, self.min_size),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        faces_found = 0

        #foreach face found in the image
        # save face to saved faces folder
        for (x, y, w, h) in faces:
            cropped_face = image[y:y + h, x:x + w]

            # show rectangle on faces
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Saving to mappings
            face_name = "face" + str(self.faceCounter) + ".jpg"
            self.mapping_dictionary[whole_image_name].append(face_name)
            self.inverse_mapping_dictionary[face_name] = whole_image_name

            # Save face image
            face_path = FACES_PATH + "/" + face_name
            cv2.imwrite(face_path, cropped_face)
            self.faceCounter += 1
            faces_found += 1


        # print("Found {0} faces!".format(facesFound))
        # self.showImage(image)


    # dirPath = absolute path to directory
    def cropImagesInDirectory(self, dirPath):
        imagesPathesToCrop = []
        for file in os.listdir(dirPath):
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                imagesPathesToCrop.append(os.path.join(dirPath, file).replace("\\", "/"))

        for imgPath in imagesPathesToCrop:
            self.cropImage(imgPath)


    #image = image object
    def showImage(self, image):
        resize_factor = 0.4

        width = int(image.shape[1] * resize_factor)
        height = int(image.shape[0] * resize_factor)
        dim = (width, height)
        # resize image
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        cv2.imshow("Faces found", image)
        cv2.waitKey(0)