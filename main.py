import multiprocessing
import os
from multiprocessing import Pipe, Process

import boto3
from gensim.models.doc2vec import Doc2Vec

from rk_brain.arxiv_db_updater.download_pdf import pdf_downlaod_main
from rk_brain.arxiv_db_updater.get_s3 import get_s3_to_s3
from rk_brain.arxiv_db_updater.rss_fetcher import rss_main
from rk_brain.contentbased_recsys.scripts.clean_metadata import (clean_df,
                                                                 parallelize_dataframe)
from rk_brain.contentbased_recsys.scripts.first_train import \
    main_Doc2vec_traning
from rk_brain.contentbased_recsys.scripts.online_train import \
    main_online_Doc2vec_traning
from rk_brain.etl.pdftotext import pdf_text_extractor
# from rk_brain.knowldgegraph.neo4j_node_builder import main_node_builder
# from rk_brain.knowldgegraph.neo4j_relationship_creator import \
    # main_relationship_creator

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
    this task is parent of two child process, first child fetch recent papers from arxiv.org. Second process will download pdf of the papers. 
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

def bulk_pdf_train_node_builder(sibling_, master_child_conn):
    '''
    This is the second parent task of the whole pipeline. It's the main task where all, text extraction, traning, building knowldge graph sub tasks are going to execute.
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
    tar_downlaoder = Process(target=s3_tar_filename, args=(child_conn,))
    BUCKET = 'arxivoverload-developement'
    for i in TAR_FILENAME:
        """
        Process designing 
        """
        tar_downlaoder = Process(target=s3.download_file, args=(BUCKET, i, 'data/tar/data.tar'))
        pdf_extractor = Process(target=pdf_text_extractor, args=(child_conn,))
        node_builder = Process(target=main_node_builder, args=(child_conn,))
        extract_etl = Process(target=main_node_builder, args=(child_conn,))
        train_doc2vec = Process(target=main_Doc2vec_traning, args=(child_conn,))
        online_train_doc2vec = Process(target=main_online_Doc2vec_traning, args=(child_conn,))
        relatioship_builder = Process(target=main_relationship_creator, args=(child_conn,))
        """
        Starting processes
        """
        tar_downlaoder.start()
        tar_downlaoder.join()
        pdf_extractor.start()
        print(parent_conn.recv())
        pdf_extractor.join()
        node_builder.start()
        print(parent_conn.recv())
        node_builder.join()


if __name__ == '__main__':
    print("Starting !!!")
    parent_conn, child_conn = Pipe()
    R_N_B = Process(target=rss_node_builder, args=(child_conn,))

    R_N_B.start()
    print(parent_conn.recv())
    R_N_B.join()

    # get_s3_to_s3()
    # pdf_text_extractor()
    # rss_main()
    # pdf_downlaod_main()
    #
    # s3_tar_filename()
    # for i in TAR_FILENAME:
    # print("Downloading,", i)
    # s3.download_file(BUCKET, i, 'data/tar/data.tar')
    # print("Downloaded,", i)
    #
    # print("Finished Downloading", i)

    # pdf_text_extractor()
    # model = Doc2Vec.load("./models/arxiv_full_text")
    # main_online_Doc2vec_traning(model)
    # online_train()
    # Do machine learning Work

    # os.system('rm -r ./data/pdf/*')
    # s3.delete_object(Bucket=BUCKET, Key=i)
    print("MISSION COMPLETE")

def main(parent_conn, child_conn):
    """
    This fuction is the master of call parent processed 
    """
    try:
        # CODE TO BE ADDED FOR PARENT 
        pass

    except Exception as e:
        print("uyg")


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    main(parent_conn, child_conn)
    