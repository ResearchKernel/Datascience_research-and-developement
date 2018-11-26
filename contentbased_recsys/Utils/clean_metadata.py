import re
from nltk.corpus import stopwords
import random
import os
import pandas as pd
import numpy as np
import nltk
import time
from multiprocessing import Pool

stop_words = set(stopwords.words('english'))

# for dataframe partition 
num_partitions = 1000 #number of partitions to split dataframe

def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool()
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def clean_df(df):
    # start = time.time()
    print('Process working on: ',os.getpid())
    df['tokenized'] = df['abstract'].apply(lambda x: apply_all(x)) + df['title'].apply(lambda x: apply_all(x))
    print('Process done:',os.getpid())
    print()
    # end = time.time()
    # print("time to complete :", end-start)
    return df

# For data cleaning 
def initial_clean(text):
    """
    Function to clean text of websites, email addresess and any punctuation
    We also lower case the text
    """
    text = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
    text = re.sub("[^a-zA-Z ]", "", text)
    text = text.lower() # lower case the text
    text = nltk.word_tokenize(text)
    return text

stop_words = stopwords.words('english')

def remove_stop_words(text):
    """
    Function that removes all stopwords from text
    """
    return [word for word in text if word not in stop_words]

def apply_all(text):
    """
    This function applies all the functions above into one
    """
    return remove_stop_words(initial_clean(text))

