import logging
import os
from multiprocessing import Pool

import gensim
import pandas as pd
from py2neo import Graph, Node, Relationship, authenticate

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# set up authentication parameters
authenticate("camelot:7474", "neo4j", "password123")

# connect to authenticated graph database
graph = Graph(password="password")

def neo_node_creator(dataframe_list_graph, graph):
    '''
    Fucntion takes dataframe
    Create nodes without any relatioships
    '''
    for i in dataframe_list_graph:
        cypher = graph.begin()
        cypher.run('create (id:paper {arxiv_id:"%s"})' % i)
        cypher.commit() 

def main_node_builder(conn):
    # pool = Pool()
    filenames_base_list = os.listdir('./data/pdf/')
    arxiv_id_filenames_base = [os.path.basename(i) for i in filenames_base_list]
    arxiv_id = [os.path.splitext(i)[0] for i in arxiv_id_filenames_base]
    # Creating zip of dataframe and graph 
    neo_node_creator(arxiv_id, graph)
#     pool.map(new_arxiv, neo_node_creator)
#     pool.close()
#     pool.merge()
    return arxiv_id