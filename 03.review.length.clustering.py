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

idx = np.random.randint(len(data), size=10)
sampled_data = data[idx,:]

def euclidean_distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

similarity_matrix = []

for i in sampled_data:
    matrix = []
    for j in sampled_data:
        matrix.append(euclidean_distance(i,j))
        
    similarity_matrix.append(matrix)

# the point in cluster 1 will be a number for the index?
def get_max_dis(cluster1, cluster2):
    max_dis = -999
    for i in cluster1:
        for j in cluster2:
            if similarity_matrix[i][j] > max_dis:
                max_dis = similarity_matrix[i][j]
    return max_dis

def d_clus(cluster):
    if all(isinstance(x, type(cluster[0])) for x in cluster):
        return cluster
    for clus in cluster:
        if not isinstance(clus, int):
            cluster.remove(clus)
            for c in clus:
                cluster.append(c)
    return d_clus(cluster)

clusted = [[i] for i in range(len(sampled_data))]
new_clusted = []
min_checked = []

def hierarchical_clustering(similarity_matrix):
    for a in range(len(similarity_matrix)):
        print("a: ", a)
        min_index = [0,0]
        try:
            min_val = 999
        except:
            min_val = 999
        print("min_checked: ", min_checked)
        # find the min 
        for i in range(len(similarity_matrix)):
            for j in range(i+1, len(similarity_matrix)):
                if similarity_matrix[i][j] < min_val and similarity_matrix[i][j] not in min_checked:
                    min_val = similarity_matrix[i][j]
                    min_index[0] = i
                    min_index[1] = j
        # merge
        if [min_index[0]] not in clusted:
            print(2)
            print("min_index: ", min_index)
            for clus in clusted:
                if min_index[0] in d_clus(clus) and min_index[1] not in d_clus(clus):
                    print("clus: ", clus)
                    clusted.remove(clus)
                    clusted.append([clus, min_index[1]])
                    print("[clus, min_index[1]]: ", [clus, min_index[1]])
                    print("clusted: ", clusted)
                    min_checked.append(min_val)
                    break
        elif [min_index[1]] not in clusted:
            print(3)
            print("min_index: ", min_index)
            for clus in clusted:
                test_clus = d_clus(clus)
                if min_index[1] in d_clus(clus) and min_index[0] not in d_clus(clus):
                    print("clus: ", clus)
                    clusted.remove(clus)
                    clusted.append([clus, min_index[0]])
                    print("[clus, min_index[0]]: ", [clus, min_index[0]])
                    print("clusted: ", clusted)
                    min_checked.append(min_val)
                    break
        else:
            print(4)
            if min_index == [0,0]:
                break
            min_checked.append(min_val)
            try:
                clusted.remove([min_index[0]])
            except:
                print("error remove j")
            try:
                clusted.remove([min_index[1]])
            except:
                print("error remove i")
            print("min_index: ", min_index)
            print("clusted: ", clusted)
            clusted.append([min_index[0], min_index[1]])

hierarchical_clustering(similarity_matrix)




