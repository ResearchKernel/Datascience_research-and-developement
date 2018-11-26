import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pandas as pd 
import gensim 
import pymysql.cursors
from py2neo import authenticate, Graph, Node, Relationship
from multiprocessing import Pool

# set up authentication parameters
authenticate("camelot:7474", "neo4j", "password123")

# connect to authenticated graph database
graph = Graph(password="password")

# Connect to the MYSQL database
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='password123',
                            db='arxivOverload',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
# create cursor to MYSQL database
cursor = connection.cursor()



def neo_node_creator(dataframe_list_graph, graph):
    '''
    Fucntion takes dataframe
    Create nodes without any relatioships
    '''
    for i in dataframe_list_graph:
        cypher = graph.begin()
        cypher.run('create (id:paper {arxiv_id:"%s"})' % i)
        cypher.commit() 

if __name__ == "__main__":
    # pool = Pool()
    # New data fetch query 
    query = "select arxiv_id,  primary_category from arxivOverload.paper_metadata where created_at > '2018-05-11 15:23:09';"
    # New data to train 
    online_dataframe = pd.read_sql(query, con=connection)
    # extaacting list from Dataframe
    new_arxiv_ids = online_dataframe['arxiv_id'].tolist()
    # Creating zip of dataframe and graph 
    neo_node_creator(new_arxiv_ids, graph)
    # pool.map(new_arxiv_ids, neo_node_creator)
    # pool.close()
    # pool.merge()
    