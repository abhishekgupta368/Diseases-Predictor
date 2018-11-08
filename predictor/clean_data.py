import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk 
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def get_review(dis):
    dset=np.array([])
    for i in range(146):
        rev = [v for v in dis[i] if str(v) != 'nan']
        string = ' '.join(rev)
        dset= np.append(dset,string)
    return dset

def get_clean_data(filepath):
    data = pd.read_csv(filepath,delimiter=',')
    dis = data.iloc[:,1:-1].values
    sym = data.iloc[:,0].values
    
    res=get_review(dis)
    val1 = pd.DataFrame(res,columns=['review'])
    val2 = pd.DataFrame(sym,columns=['symptom'])
    
    result = pd.concat([val1,val2],axis=1)
    
    result.to_csv('clean_data.csv')