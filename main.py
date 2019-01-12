import datetime
import multiprocessing
import os
from multiprocessing import Pipe, Process

import boto3

from gensim.models.doc2vec import Doc2Vec
from rk_brain.arxiv_db_updater.download_pdf import pdf_downlaod_main
from rk_brain.arxiv_db_updater.get_s3 import get_s3_to_s3
from rk_brain.arxiv_db_updater.pdf_metadata_fetcher import pdf_main
from rk_brain.arxiv_db_updater.rss_fetcher import rss_main
from rk_brain.contentbased_recsys.scripts.clean_metadata import (clean_df,
                                                                 parallelize_dataframe)
from rk_brain.contentbased_recsys.scripts.first_train import \
    main_Doc2vec_traning
from rk_brain.contentbased_recsys.scripts.online_train import \
    main_online_Doc2vec_traning
from rk_brain.etl.pdftotext import pdf_text_extractor
from rk_brain.knowldgegraph.neo4j_node_builder import main_node_builder
from rk_brain.knowldgegraph.neo4j_relationship_creator import \
    main_relationship_creator

s3 = boto3.client('s3')
TAR_FILENAME = []
def s3_tar_filename():
    BUCKET = 'arxivoverload-developement'
    PREFIX = 'machine-learning-service/pdf/pdf/'
    print("workin in listing")
    result = s3.list_objects(Bucket=BUCKET,
                             Prefix=PREFIX,
                             Delimiter='/')
    try:
        for j in range(1, 1000):
            TAR_FILENAME.append(result["Contents"][j]["Key"])
    except Exception as identifier:
        pass
    print("Done this")


def rss_fetcher_pdf_downloader(master_child_conn):
    '''
    This is first parent task of the whole pipeline. 
    Functions takes a master child connection. 
    this task is parent of two child process, first child fetch recent papers from arxiv.org. 
    Second process will download pdf of the papers. 
    '''
    parent_conn, child_conn = Pipe()
    rss = Process(target=rss_main, args=(child_conn,))
    pdf_downlaoder = Process(target=pdf_downlaod_main, args=(child_conn,))
    rss.start()
    print(parent_conn.recv())
    rss.join()
    pdf_downlaoder.start()
    print(parent_conn.recv())
    pdf_downlaoder.join()
    master_child_conn.send("DONE RSS PHASE!!!")
    master_child_conn.close()

def bulk_pdf_train_node_builder(master_parent_conn, master_child_conn):
    '''
    This is the second parent task of the whole pipeline. It's the main task where all
    text extraction, traning, building knowldge graph sub tasks are going to execute.
    Function takes sibling task connection, and master child connection as a parameters.
    this task is parent of nine child process: 
        1. Downloaing tarfile from s3.
        2. downloaing metadata of pdf.
        3. Waiting for sibling parent task to finish.
        4. Extracting text and references from pdf.
        5. building node in knowldge graph.
        5. traning/online train doc2vec model.
        7. using trained model to create relationship in knowldge graph.
        8. creating properties of node in knowldge graph using extracted references.
        9. creating properties of node in knowldge graph from downloaded metadata.
    '''
    BUCKET = 'arxivoverload-developement'
    FILENAME = '/machine-learning-service/extracted_data/'+ str(datetime.date.today()) + '.zip'
    parent_conn, child_conn = Pipe()
    for i in TAR_FILENAME:
        tar_downlaoder = Process(target=s3.download_file, args=(BUCKET, i, 'data/tar/data.tar'))                         # Process for Downlaod tafile from S3 to Local machine.
        pdf_metadata_fetcher = Process(target=pdf_main, args=(child_conn,))                                              # Process for get metadata of PDF's. 
        pdf_extractor = Process(target=pdf_text_extractor, args=(child_conn,))                                           # Process for extracting text and references from PDF.
        node_builder = Process(target=main_node_builder, args=(child_conn,))                                             # Process for building nodes in knowledge graph.
        train_doc2vec = Process(target=main_Doc2vec_traning, args=(child_conn,))                                         # Process for traning  Doc2vec model. 
        online_train_doc2vec = Process(target=main_online_Doc2vec_traning, args=(child_conn,))                           # process for traning online Doc2vec.
        keyword_generator = Process(target=keyword_generator, args=(child_conn,))                                        # Process for extrating keywords from textfile. 
        # metadata_relatioship_builder = Process(target=metadata_relationship_creator, args=(child_conn,))               # Process for building metadata relatioship generator.  
        
        # Starting downloading from S3 to local machine
        tar_downlaoder.start()                                                                                           
        tar_downlaoder.join() 
        # Start downlading  
        pdf_metadata_fetcher.start()  
        print(master_child_conn.revc())     
        pdf_metadata_fetcher.join()   
        
        # getting status from master parent processs 1 and then closing it. 
        print(master_parent_conn.recv())
        master_child_conn.join()
        # and closing the first master process.

        # starting extraction task 
        pdf_extractor.start() # start extrating pdf to /data/pdf folder. 
        print(parent_conn.recv())
        pdf_extractor.join()

        # starting node builder for knowldge graph 
        node_builder.start()
        print(parent_conn.recv())
        node_builder.join()

        # checking if this is the first time model traning 
        if len (os.listdir("./models/")) == 0:
            # starting doc2vec traning 
            train_doc2vec.start()
            model = parent_conn.recv()
            train_doc2vec.join()
        else:
            
            online_train_doc2vec.start()
            model = parent_conn.recv()
            online_train_doc2vec.join()
        
        # builing similarity relation between nodes
        relatioship_builder = Process(target=main_relationship_creator, args=(model, child_conn,))                        # Process for builing relationship in knowldge graph.
        relatioship_builder.start()
        print(parent_conn.recv())
        relatioship_builder.join()

        os.system('zip -r '+str(datetime.date.today())+'.zip ./data/pdf/ ./data/references/ ./data/text/')
        os.system('rm -r ./data/pdf/*')
        os.system('rm -r ./data/references/*')
        os.system('rm -r ./data/text/*')
        s3.upload_file(str(datetime.date.today()), BUCKET, FILENAME)
        s3.delete_object(Bucket=BUCKET, Key=i)

def main(parent_conn, child_conn):
    """
    This fuction is the master of call parent processed 
    """
    try:
        master_parent_process_1 = Process(target=rss_fetcher_pdf_downloader, args=(child_conn,))
        master_parent_process_2 = Process(target=bulk_pdf_train_node_builder, args=(parent_conn, child_conn,))
        # Starting master_parent_process_1 
        master_parent_process_1.start()
        print(master_parent_conn.recv())
        master_parent_process_1.join()
        
        # Starting master_parent_process_2
        master_parent_process_2.start()
        print(master_parent_conn.recv())
        master_parent_process_2.join() 
        child_conn.send("")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    master_parent_conn, master_child_conn = Pipe()
    main(master_parent_conn, master_child_conn)