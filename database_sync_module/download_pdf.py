import pandas as pd 
import boto3
from datetime import datetime
import multiprocessing
import requests
s3 = boto3.client('s3')
PATH = "../data/pdf/"

def downlaod(names):
    filename, link = names
    response = requests.get(link, stream=True)
    with open(PATH+filename, "wb") as pdf:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
def pdf_downlaod():
    link_filename = []
    csv_filename = 'data-engineering-service/arxivdailysync/' + str(datetime.date.today()) + '_pdf.csv'
    data = pd.read_csv(csv_filename)
    pdf_links = data["pdf_link"].to_list()
    pdf_name = data["arxiv_id"].to_list()
    for filename, link in zip(pdf_name, pdf_links):
        link_filename.append((filename, link))
    return link_filename

def pdf_downlaod_main():
    pool = multiprocessing.Pool()
    names = pdf_downlaod()
    try:
        result = pool.map(names, downlaod)
        pool.close()
        pool.join()
    except Exception as e:
        print(e)
        pass
