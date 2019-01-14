import logging
import os
import time
from multiprocessing import Pool

import gensim
import pandas as pd
from py2neo import Graph, Node, Relationship

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

graph = Graph(password="1234")

def neo_node_creator(arxiv_id):
        cypher = graph.begin()
        print("Runing Cypher")
        cypher.run('create (id:paper {arxiv_id:"%s"})' % arxiv_id)
        print("yess,  running")
        cypher.commit() 
        print("commited again !!!")
        print("Done ",arxiv_id)
        time.sleep(0.001)

def main_node_builder(conn):
    pool = Pool(1)
    filenames_base_list = []
    for (dirpath, dirnames, filenames) in os.walk("data/pdf/"):
            filenames_base_list += [os.path.join(dirpath, file) for file in filenames]
    arxiv_id_filenames_base = [os.path.basename(i) for i in filenames_base_list[1:]]
    arxiv_id = [os.path.splitext(i)[0] for i in arxiv_id_filenames_base]
    print("done arxiv ID")
    pool.map(neo_node_creator,arxiv_id)
    pool.close()
    pool.join()
    conn.send(arxiv_id)