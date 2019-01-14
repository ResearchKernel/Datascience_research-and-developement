import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pandas as pd 
import gensim 
from py2neo import Graph, Node, Relationship

# connect to authenticated graph database
graph = Graph(password="password")

def neo_relationship_creator(dataframe, model, graph):
    '''
    Fucntion takes dataframe, models and graph.
    Create relatioships with existing node 
    '''
    tx = graph.begin()
    for i in dataframe:
        similarity = model.docvecs.most_similar(i)
        for j, k in similarity:
            tx.run('match (id:paper {arxiv_id:"%s"})' %i +'- [:SIMILARITY_TO {similarity_score:"%s"}]' %k+ '-> (id_1:paper {arxiv_id:"%s"})' %j) # cypher query fro creating relationships 
            tx.commmit()

def main_relationship_creator(arxiv_ids, model, conn):
    neo_relationship_creator(arxiv_ids, model, graph)
    conn.send("done building similarity relationship")

