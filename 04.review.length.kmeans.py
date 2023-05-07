# for more information you can check this kaggle file: https://www.kaggle.com/hiuquang/labwork-1-data-mining

import numpy as np 
import pandas as pd 
import sys
import time
import string
import nltk
import math
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

def make_random_centroid(data, k):
    centroids = {}
    for i in range(k):
        x_range = (min(sampled_data[:,0]), max(sampled_data[:,0]))
        x = random.uniform(*x_range)
        
        y_range = (min(sampled_data[:,1]), max(sampled_data[:,1]))
        y = random.uniform(*y_range)
        
        centroids[i] = [x, y]
    
    return centroids

init_cen = make_random_centroid(sampled_data, 3)

cont = True

clusters = {}

count = 0
while cont == True:
    print("==============" + str(count) + "=============")
    list_dis = []
    dis_cen = []
    clusters = {}
    for point in sampled_data:
        dis_k = []
        for k, v in init_cen.items():
            dis_k.append(euclidean_distance(point, v))
        min_value = min(dis_k)
        min_index = dis_k.index(min_value)
        try:
            clusters[min_index].append(point)
        except:
            clusters[min_index] = [point]
    new_centroid = {}
    for k, v in init_cen.items():
        new_centroid[k] = np.mean(clusters[k], axis=0)
    
    for k in range(k):
        dis_cen.append(euclidean_distance(init_cen[k], new_centroid[k]))
    
    if all(elem < 1e-6 for elem in dis_cen):
        cont = False
    
    init_cen = new_centroid
    count += 1
    

    import matplotlib.pyplot as plt

colors = ['red', 'green', 'blue']

for label, points in clusters.items():
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    plt.scatter(x_coords, y_coords, color=colors[label])

plt.title('Scatter Plot of Points')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

plt.show()




