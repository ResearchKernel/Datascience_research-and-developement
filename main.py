from database_sync_module.pdf_metadata_fetcher import pdf_main
from database_sync_module.rss_fetcher import rss_main
from database_sync_module.download_pdf import pdf_downlaod_main
from database_sync_module.get_s3 import get_s3_to_local
from data.pdftotext import pdf_text_extractor
from contentbased_recsys.scripts import online_train
from threading import Thread
import os

"""
Tasks to do: 

1. run rss_main -> 
2. run pdf_main -> 
3. downlaod_pdf ->
4. get PDF -> 
5. ETL -> 
6. traning -> 
7. neo4j ->

"""
def do_rss():
    rss_main()

def do_pdf():
    pdf_main()

def downlaod_pdf():
    pdf_downlaod_main()

def get_pdf():
    get_s3_to_local()
 
def ETL():
    pdf_text_extractor()

def model_traning():
    online_train()

def model_to_neo4j():
    print()


def main():
    print()

if __name__ == '__main__':
    main()