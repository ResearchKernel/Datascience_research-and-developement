import multiprocessing
import os

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
from rk_brain.knowldgegraph.neo4j_node_builder import main_node_builder
from rk_brain.knowldgegraph.neo4j_relationship_creator import main_relationship_creator

s3 = boto3.client('s3')

# HELPER FUNCTIONS
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

def main():
    rss_main()
    pdf_downlaod_main()

if __name__ == '__main__':
    # get_s3_to_s3()
    # pdf_text_extractor()
    # rss_main()
    # pdf_downlaod_main()
    # BUCKET = 'arxivoverload-developement'
    # s3_tar_filename()
    # for i in TAR_FILENAME:
    # print("Downloading,", i)
    # s3.download_file(BUCKET, i, 'data/tar/data.tar')
    # print("Downloaded,", i)
    # os.system('tar -xvf ./data/tar/data.tar --directory ./data/pdf')
    # print("Finished Downloading", i)

    # pdf_text_extractor()
    # model = Doc2Vec.load("./models/arxiv_full_text")
    # main_online_Doc2vec_traning(model)
    # online_train()
    # Do machine learning Work

    # os.system('rm -r ./data/pdf/*')
    # s3.delete_object(Bucket=BUCKET, Key=i)
    print("MISSION COMPLETE")
    
