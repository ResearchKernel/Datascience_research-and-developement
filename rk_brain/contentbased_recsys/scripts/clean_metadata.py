import os
import random
import re
import time
from multiprocessing import Pool

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# for dataframe partition 
num_partitions = 10000 #number of partitions to split dataframe

def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool()
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def clean_df(df):
    # need to change for df neutral
    df['content'] = df['content'].apply(lambda x: apply_all(x))
    return df

# For data cleaning 
def stop_words_removal(text):
    """
    Function to clean text of websites, email addresess and any punctuation
    We also lower case the text
    """
    text = re.sub(r"((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
    text = re.sub(r'\b\w{1,3}\b', '',text)
    text = re.sub("[^a-zA-Z ]", " ", text)
    text = text.lower() # lower case the text
    text = nltk.word_tokenize(text)
    text = [word for word in text if word not in stop_words]
    return text

def lemmatizing(text):
    lemma_text = []
    for x in text:
        lemma_text.append(lemmatizer.lemmatize(x))
    return lemma_text 

def apply_all(text):
    """
    This function applies all the functions above into one
    """
    return lemmatizing(stop_words_removal(text))