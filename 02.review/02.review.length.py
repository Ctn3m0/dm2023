# for more information you can check this kaggle file: https://www.kaggle.com/hiuquang/labwork-1-data-mining

import numpy as np 
import pandas as pd 
import sys
import time
import string
import nltk
import matplotlib.pyplot as plt
import math
from sklearn import preprocessing as pre

review = pd.read_json("myfile_dx", lines=True)

documents = review["text"]

# remove punctuation
def remove_punc(text):
    document="".join([i for i in text if i not in string.punctuation])
    return document

documents= documents.apply(lambda x:remove_punc(x))

documents= documents.apply(lambda x: x.lower())

import nltk

stopwords = nltk.corpus.stopwords.words('english')

# remove stop words
def remove_stpw(text):
    tokens = []
    for i in text.split():
        if i not in stopwords:
            tokens.append(i)
    return tokens

documents= documents.apply(lambda x:remove_stpw(x))

length = {}
for doc in documents:
    l = len(doc)
    try:
        length[l] += 1
    except:
        length[l] = 1

def mean(x) :
    length = 0
    total = 0
    for i in x:
        length += 1
        total += i
    return total/length

def variance(x):
    m = mean(x)
    var = 0
    length = 0
    for i in x:
        length += 1
        var += i**2 - m**2
    return var/length

m = mean(length.values())

var = variance(length.values())

percent_length = {}

for k,v in length.items():
    percent_length[k] = length[k]/len(documents)

# # Create an array of x values from -3*sigma to 3*sigma
# x = np.linspace(m - 3*math.sqrt(var), m + 3*math.sqrt(var), 500)

# # Calculate the y values using the bell curve formula
# y = (1/(math.sqrt(var)*np.sqrt(2*np.pi))) * np.exp(-(x-m)**2/(2*math.sqrt(var)**2))

# # Plot the curve
# plt.plot(x, y)


plt.bar(list(percent_length.keys()), percent_length.values(), color='g')
plt.savefig("02.review.length.pdf", format="pdf", bbox_inches="tight")
plt.show()