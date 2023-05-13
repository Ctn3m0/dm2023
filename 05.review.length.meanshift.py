# for more information you can check this kaggle file: https://www.kaggle.com/hiuquang/labwork-1-data-mining

import numpy as np 
import pandas as pd 
import math
import random
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# make data for clustering
business = pd.read_json("/kaggle/input/yelp-dataset/yelp_academic_dataset_business.json", lines=True)

data = business[["latitude", "longitude", "stars", "review_count", "is_open"]]
sc = StandardScaler()
 
data = sc.fit_transform(data)
 
pca = PCA(n_components = 2)
 
data = pca.fit_transform(data)

def euclidean_distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

idx = np.random.randint(len(data), size=500)
sampled_data = data[idx,:]

def euclidean_distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

idx = np.random.randint(len(data), size=500)
sampled_data = data[idx,:]

n = len(sampled_data)

def kernel(bandwidth, dis):
    if dis < bandwidth:
        return 1
    else: 
        return 0

def shiftMode(data, pre, bandwidth):
#     mode = (x*kernel(bandwidth, euclidean_distance(x, pre)) for x in sampled_data)/(kernel(bandwidth, euclidean_distance(x, pre)) for x in sampled_data)
    numerator = 0
    denominator = 0
    for x in data:
        kernel_value = kernel(bandwidth, euclidean_distance(x, pre))
        numerator += x * kernel_value
        denominator += kernel_value
    mode = numerator / denominator
    return mode

mode = [[0 for j in range(n)] for i in range(n)]

threshold = 1e-6
bandwidth = 1
# mode = [[]]

for i in range(n):
    m = 0
    mode[i][m] = sampled_data[i]
    flag = True
    while flag == True:
        mode[i][m+1] = shiftMode(sampled_data, mode[i][m], bandwidth)
        m = m+1
        if euclidean_distance(mode[i][m], mode[i][m-1]) < threshold:
            flag = False
    mode[i][0] = mode[i][m]
    
clusters = []
for i in range(n):
    if tuple(mode[i][0]) not in clusters:
        clusters.append(tuple(mode[i][0]))

print(clusters)

