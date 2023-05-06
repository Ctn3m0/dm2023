# for more information you can check this kaggle file: https://www.kaggle.com/hiuquang/labwork-1-data-mining

import numpy as np 
import pandas as pd 
import sys
import time
import string
import nltk

# review = pd.read_json("../input/yelp-dataset/yelp_academic_dataset_review.json", lines=True, chunksize = 100)
review = pd.read_json("myfile_aa", lines=True)

documents = review["text"]

def remove_punc(text):
    document="".join([i for i in text if i not in string.punctuation])
    return document

documents= documents.apply(lambda x:remove_punc(x))

# lower the text
documents= documents.apply(lambda x: x.lower())

stopwords = nltk.corpus.stopwords.words('english')
# remove stop words
def remove_stpw(text):
    tokens = []
    for i in text.split():
        if i not in stopwords:
            tokens.append(i)
    return tokens

documents= documents.apply(lambda x:remove_stpw(x))

# calculate DF
DF = {}
total_no_doc = len(documents)
for i in range(len(documents)):
    unique_tokens = np.unique(documents[i])
    for w in unique_tokens:
        try: 
            DF[w] += 1
        except:
            DF[w] = 1

first_10_items = list(DF.items())[:10]
print(first_10_items)

# calculate IDF
IDF = {}
for key, value in DF.items():
    IDF[key] = np.log(total_no_doc/DF[key]) # plus 1 for the case of 0 ?

first_10_items = list(IDF.items())[:10]
print(first_10_items)

# calculate TF
documents_tf = []
for i in range(len(documents)):
    TF = {}
    words = {}
    len_doc = len(documents[i])
    
    for word in documents[i]:
        try: 
            words[word] += 1
        except:
            words[word] = 1
            
    for k, v in words.items():
        TF[k] = words[k]/len_doc
        
    documents_tf.append(TF)

# calculate TF-IDF
documents_tf_idf = []
for doc_tf in documents_tf:
    TF_IDF = {}
    for k, v in doc_tf.items():
        TF_IDF[k] = doc_tf[k] * IDF[k]
        
    documents_tf_idf.append(TF_IDF)

print(documents_tf_idf[0])
print(documents_tf[0])
print(np.unique(documents[0], return_counts = True))


