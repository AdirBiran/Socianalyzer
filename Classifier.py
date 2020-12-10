import matplotlib.pyplot as plt
import numpy
import scipy.cluster.hierarchy as hcluster

from Extractor import Extractor
from Settings import *
from collections import Counter

# generate 3 clusters of each around 100 points and one orphan point
N=100
data = numpy.random.randn(3*N,2)
data[:N] += 5
data[-N:] += 10
data[-1:] -= 20

ext = Extractor()
dirPath = FACES_PATH
ext.extractFeaturesFromDirectory(dirPath)
data = ext.faces_encodings
data_numpy = numpy.array([])

for face in data:
    data_numpy = numpy.concatenate((data_numpy, face))

data_numpy = data_numpy.reshape(len(data), 128)

# clustering
thresh = 0.4
clusters = hcluster.fclusterdata(data_numpy, thresh)
print(clusters)
duplicates = [item for item, count in Counter(clusters).items() if count > 1]
print(duplicates)

