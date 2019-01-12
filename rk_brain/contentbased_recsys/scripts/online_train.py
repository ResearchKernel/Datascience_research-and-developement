import json
import logging
import os
import random
import time
from collections import namedtuple
from multiprocessing import Pool

import pandas as pd
from gensim import corpora, models, similarities
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from rk_brain.contentbased_recsys.scripts.clean_metadata import (clean_df,
                                                                 parallelize_dataframe)

'''
Reading textfiles from folder and making dataframe from it 
'''

# model = Doc2Vec.load("./models/final_model")
# arxiv_id_tags = model.docvecs.doctags


def online_Doc2vec_traning(dataframe, model):
    tagged_docs = []
    analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
    for text, tags in zip(dataframe['content'].tolist(), dataframe['filename'].tolist()):
        tags = [tags]
        tagged_docs.append(analyzedDocument(text, tags))
    model.build_vocab(tagged_docs, update=True)  # Building vocabulary
    alpha_val = 0.025        # Initial learning rate
    min_alpha_val = 1e-4     # Minimum for linear learning rate decay
    passes = 15              # Number of passes of one document during training
    alpha_delta = (alpha_val - min_alpha_val) / (passes - 1)

    for epoch in range(passes):

        # Shuffling gets better results

        random.shuffle(tagged_docs)

        # Train

        model.alpha, model.min_alpha = alpha_val, alpha_val

        model.train(tagged_docs, total_examples=model.corpus_count,
                    epochs=model.epochs)

        # Logs

        print('Completed pass %i at alpha %f' % (epoch + 1, alpha_val))

        # Next run alpha

        alpha_val -= alpha_delta

    model.save("./models/arxiv_full_text")
    print("Model Saved into Disk")
    return model

def dataframe_maker():
    filenames = os.listdir("./data/text/")
    dataframe_dict_list = []
    for i in filenames[1:]:   # for excluding .DS_Store
        dataframe_dict = {}
        file_path = "./data/text/"+i
        f = open(file_path, "r")
        text = f.read()
        dataframe_dict["filename"] = i
        dataframe_dict["content"] = text
        dataframe_dict_list.append(dataframe_dict)
        f.close()
        text = None
    data = pd.DataFrame(dataframe_dict_list)
    dataframe_dict_list = []
    data = parallelize_dataframe(data.head(), clean_df)
    return data
def main_online_Doc2vec_traning(model, conn):
    data = dataframe_maker()
    model = online_Doc2vec_traning(data, model)
    

