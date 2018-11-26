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

# Connect to the MYSQL database
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='password123',
                            db='arxivOverload',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
# create cursor to MYSQL database
cursor = connection.cursor()



def neo_node_creator(dataframes, graph):
    '''
    Fucntion takes dataframe
    Create nodes without any relatioships
    '''
    for dataframe, category_name, model, graph in zip(dataframes, category_names, models, graph):
        for i in dataframe['arxiv_id']:
            

            
    







if __name__ == "__main__":
    query = "select arxiv_id,  primary_category from arxivOverload.paper_metadata where created_at > '2018-05-11 15:23:09';"

    # New data to train 
    online_dataframe = pd.read_sql(query, con=connection)

    # Categorty Dataframes
    astro_ph_df = online_dataframe.loc[online_dataframe.primary_category.str.contains("astro-ph.")]
    cond_mat_df = online_dataframe.loc[online_dataframe.primary_category.str.contains("cond-mat.")]
    esss_df     = online_dataframe.loc[online_dataframe.primary_category.str.contains("esss.")]
    econ_df     = online_dataframe.loc[online_dataframe.primary_category.str.contains("econ.")]
    cs_df       = online_dataframe.loc[online_dataframe.primary_category.str.contains("cs.")]
    hep_df      = online_dataframe.loc[online_dataframe.primary_category.str.contains("hep-")]
    maths_df    = online_dataframe.loc[online_dataframe.primary_category.str.contains("math.")]
    physics_df  = online_dataframe.loc[online_dataframe.primary_category.str.contains("physics.")]
    nlin_df     = online_dataframe.loc[online_dataframe.primary_category.str.contains("nlin.")]
    nucl_df     = online_dataframe.loc[online_dataframe.primary_category.str.contains("nucl-")]
    q_bio_df    = online_dataframe.loc[online_dataframe.primary_category.str.contains("q-bio.")]
    stats_df    = online_dataframe.loc[online_dataframe.primary_category.str.contains("stats.")]
    q_fin_df    = online_dataframe.loc[online_dataframe.primary_category.str.contains("q-fin.")]
    quant_ph_df = online_dataframe.loc[online_dataframe.primary_category.str.contains("quant-")]
    gr_qc_df    = online_dataframe.loc[online_dataframe.primary_category.str.contains("gr-")]
    # Creating list of dataframes and caegrories
    dataframes     = [astro_ph_df, cond_mat_df, esss_df, econ_df, cs_df, hep_df, maths_df, physics_df, nlin_df, nucl_df, q_bio_df, stats_df, q_fin_df, quant_ph_df, gr_qc_df]
    category_names = ['astro_ph', 'cond_mat', 'esss', 'econ', 'cs', 'hep', 'maths', 'physics', 'nlin', 'nucl', 'q_bio', 'stats', 'q_fin', 'quant_ph', 'gr_qc']
    models         = ['astro_ph_model', 'cond_mat_model', 'esss_model', 'econ_model', 'cs_model', 'hep_model', 'maths_model', 'physics_model', 'nlin_model', 'nucl_model', 'q_bio_model', 'stats_model', 'q_fin_model', 'quant_ph_model', 'gr_qc_model']
    neo_node_creator(dataframe, graph)

# tx = graph.begin()


# tx.run("")

