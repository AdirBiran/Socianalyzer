import cv2
from Settings import *


class Cropper:
    def __init__(self, min_size=50):
        self.cascPath = os.path.join(RESOURCES_PATH, 'haarcascade_frontalface_default.xml')
        self.faceCounter = 1
        self.min_size = min_size

    #imagePath = absolute path to image
    def cropImage(self, imagePath):
        faceCascade = cv2.CascadeClassifier(self.cascPath)
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(self.min_size, self.min_size),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        facesFound = 0

        #foreach face found in the image
        # save face to saved faces folder
        for (x, y, w, h) in faces:
            cropped_face = image[y:y + h, x:x + w]

            # show rectangle on faces
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imwrite(FACES_PATH + "/face" + str(self.faceCounter) + ".jpg", cropped_face)
            self.faceCounter += 1
            facesFound += 1

        #print("Found {0} faces!".format(facesFound))
        #self.showImage(image)

    #dirPath = absolute path to directory
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



