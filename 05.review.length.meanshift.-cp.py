import numpy as np 
import pandas as pd 
import sys
import time
import nltk

# review = pd.read_json("../input/yelp-dataset/yelp_academic_dataset_review.json", lines=True, chunksize = 100)
review = pd.read_json("myfile_dx", lines=True)

documents = review["text"]
documents

stopwords = nltk.corpus.stopwords.words('english')
# remove stop words
def remove_stpw(text):
    tokens = []
    for i in text.split():
        if i not in stopwords:
            tokens.append(i)
    return tokens

documents= documents.apply(lambda x:remove_stpw(x))
documents.head()

l = []
for i in documents:
    l.append(len(i))
    
def euclidean_distance(x, y):
    return x - y

n = len(documents)

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

mode = [[] for i in range(n)]

threshold = 1
bandwidth = 3
# mode = [[]]

for i in range(n):
    m = 0
    mode[i].append(l[i])
    flag = True
    while flag == True:
        mode[i].append(shiftMode(l, mode[i][m], bandwidth)) # change to append
        m = m+1
        if euclidean_distance(mode[i][m], mode[i][m-1]) < threshold:
            flag = False
    mode[i][0] = mode[i][m]
    
clusters = []
for i in range(n):
    if tuple(mode[i][0]) not in clusters:
        clusters.append(tuple(mode[i][0]))

