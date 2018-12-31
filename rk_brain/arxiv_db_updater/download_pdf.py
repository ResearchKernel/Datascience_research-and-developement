import pandas as pd 
import boto3
import datetime
import multiprocessing
import requests
import logging
DEFAULT_LEVEL = logging.DEBUG
formatter = logging.Formatter("%(levelname)s: %(asctime)s - %(name)s - %(process)s - %(message)s")
s3 = boto3.client('s3')
PATH = "data/pdf/"

def downlaod(names):
    filename, link= names
    response = requests.get(link, stream=True)
    with open(PATH+filename+".pdf", "wb") as pdf:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    
def pdfs_to_downlaod():
    link_filename = []
    csv_filename = 'data/daily_update/' + str(datetime.date.today()) + '.csv'
    data = pd.read_csv(csv_filename)
    pdf_links = data["pdf_link"]
    pdf_name = data["arxiv_id"]
    for filename, link in zip(pdf_name, pdf_links):
        link_filename.append((filename, link))
    return link_filename

def pdf_downlaod_main():
    pool = multiprocessing.Pool()
    names = pdfs_to_downlaod()
    names = names
    try:
        pool.map(downlaod,names)
        pool.close()
        pool.join()
    except Exception as e:
        print(e)
        pass

