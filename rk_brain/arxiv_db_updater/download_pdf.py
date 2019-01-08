import pandas as pd 
import boto3
import datetime
import multiprocessing
import requests
import logging
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
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
    try:
        csv_filename = 'data/daily_update/' + str(datetime.date.today()) + '.csv'
        data = pd.read_csv(csv_filename)
        pdf_links = data["pdf_link"]
        pdf_name = data["arxiv_id"]
        for filename, link in zip(pdf_name, pdf_links):
            link_filename.append((filename, link))
        return link_filename
    except Exception as e:
        print(e)
        print("Probably arxiv RSS is down!!!")
    

def pdf_downlaod_main(conn):
    pool = multiprocessing.Pool()
    names = pdfs_to_downlaod()
    names = names
    try:
        pool.map(downlaod,names)
        pool.close()
        pool.join()
        conn.send("Finished downloading all PDF of recently published papers!!! ")
    except Exception as e:
        conn.send("Problem in downloading all PDF of recently published papers, Error Stack printing below")
        print(e)
        conn.close()
        pass

