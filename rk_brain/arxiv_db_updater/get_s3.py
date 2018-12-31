import os
import xml.etree.ElementTree

def get_s3_to_s3():
    os.system("s3cmd get --requester-pays s3://arxiv/pdf/arXiv_pdf_manifest.xml --force")
    e = xml.etree.ElementTree.parse('arXiv_pdf_manifest.xml').getroot()
    for i in e.findall('file'):
        date = i.find('filename').text
        if "arXiv_pdf_18" in date:
            os.system("aws s3 cp s3://arxiv/"+i.find('filename').text+" "+"s3://arxivoverload-developement/machine-learning-service/pdf/"+i.find('filename').text+""+" --request-payer")