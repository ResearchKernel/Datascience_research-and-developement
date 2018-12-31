import os
import boto3
from rk_brain.etl.pdftotext import pdf_text_extractor
from rk_brain.arxiv_db_updater.rss_fetcher import rss_main
from rk_brain.arxiv_db_updater.get_s3 import get_s3_to_s3
from rk_brain.arxiv_db_updater.download_pdf import pdf_downlaod_main 

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
    print("DONe this")

# def main():
#     get_s3_to_s3()
#     rss_main()
#     pdf_downlaod_main()


if __name__ == '__main__':
    s3 = boto3.client('s3')
    BUCKET = 'arxivoverload-developement'
    s3_tar_filename()
    for i in TAR_FILENAME:
        s3.download_file(BUCKET, i,'data/tar/data.tar')
        os.system('tar -xvf ./data/tar/data.tar --directory ./data/pdf')
        os.system('rm -r ./data/pdf/*')
        s3.delete_object(Bucket=BUCKET, Key=i)
        print("MISSION COMPLETE")
