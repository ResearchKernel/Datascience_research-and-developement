import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pandas as pd 
import gensim 
import pymysql.cursors
from py2neo import authenticate, Graph, Node, Relationship

# set up authentication parameters
authenticate("camelot:7474", "neo4j", "password123")

# connect to authenticated graph database
graph = Graph(password="password")




def neo_relationship_creator(dataframe, models, graph):
    '''
    Fucntion takes dataframe, models and graph.
    Create relatioships with existing node 
    '''
    for dataframe, model, graph in zip(dataframe, models,graph):
        tx = graph.begin()
        for i in dataframe['arxiv_id']:
            similarity = model.docvecs.most_similar(i)
            for j, k in similarity:
                tx.run('match (id:paper {arxiv_id:"%s"})' %i +'- [:SIMILARITY_TO {similarity_score:"%s"}]' %k+ '-> (id_1:paper {arxiv_id:"%s"})' %j) # cypher query fro creating relationships 
                tx.commmit()

def main_relationship_creator(arxiv_id, model):
    dataframes     = [arxiv_id]
    models         = [model]
    neo_relationship_creator(dataframes, models, graph)

# tx = graph.begin()


# tx.run("")

