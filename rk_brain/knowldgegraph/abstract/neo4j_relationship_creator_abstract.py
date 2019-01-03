import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pandas as pd 
from py2neo import authenticate, Graph, Node, Relationship
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# set up authentication parameters
authenticate("camelot:7474", "neo4j", "password123")

# connect to authenticated graph database
graph = Graph(password="password")



def neo_relationship_creator(dataframe, models):
    '''
    Fucntion takes dataframe, models and graph.
    Create relatioships with existing node 
    '''
    for dataframe, model in zip(dataframe, models):
        for i in dataframe['arxiv_id']:
            print(type(model))
            similarity = model.docvecs.most_similar(i)
            for j, k in similarity:
                cypher = graph.begin()
                cypher.run('match (id:paper {arxiv_id:"%s"}) create (id)' %i +'- [:SIMILARITY_TO {similarity_score:"%s"}]' %k+ '-> (id_1:paper {arxiv_id:"%s"})' %j) # cypher query fro creating relationships 
                cypher.commit()


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

    #Loading Models 
    astro_ph_model          = Doc2Vec.load('../../models/Abstract/astro_ph')
    cond_mat_model          = Doc2Vec.load('../../models/Abstract/cond_mat')
    # esss_model              = Doc2Vec.load('../../models/Abstract/esss')
    # econ_model              = Doc2Vec.load('../../models/Abstract/econ') 
    # cs_model                = Doc2Vec.load('../../models/Abstract/cs')
    # hep_model               = Doc2Vec.load('../../models/Abstract/hep')
    # maths_model             = Doc2Vec.load('../../models/Abstract/maths')
    # physics_model           = Doc2Vec.load('../../models/Abstract/physics')
    # nlin_model              = Doc2Vec.load('../../models/Abstract/nlin')
    # nucl_model              = Doc2Vec.load('../../models/Abstract/nucl')
    # q_bio_model             = Doc2Vec.load('../../models/Abstract/q_bio')
    # stats_model             = Doc2Vec.load('../../models/Abstract/stats')
    # q_fin_model             = Doc2Vec.load('../../models/Abstract/q_fin')
    # quant_ph_model          = Doc2Vec.load('../../models/Abstract/quant_ph')
    # gr_qc_model             = Doc2Vec.load('../../models/Abstract/gr_qc')

    # Creating list of dataframes and caegrories
    # dataframes     = [astro_ph_df, cond_mat_df, esss_df, econ_df, cs_df, hep_df, maths_df, physics_df, nlin_df, nucl_df, q_bio_df, stats_df, q_fin_df, quant_ph_df, gr_qc_df]
    # category_names = ['astro_ph', 'cond_mat', 'esss', 'econ', 'cs', 'hep', 'maths', 'physics', 'nlin', 'nucl', 'q_bio', 'stats', 'q_fin', 'quant_ph', 'gr_qc']
    # models         = ['astro_ph_model', 'cond_mat_model', 'esss_model', 'econ_model', 'cs_model', 'hep_model', 'maths_model', 'physics_model', 'nlin_model', 'nucl_model', 'q_bio_model', 'stats_model', 'q_fin_model', 'quant_ph_model', 'gr_qc_model']
    
    dataframes     = [astro_ph_df, cond_mat_df]
    models         = [astro_ph_model, cond_mat_model]

    neo_relationship_creator(dataframes, models)

