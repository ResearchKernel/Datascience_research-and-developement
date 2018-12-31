import os
import sys
import time
import json
import shutil
import multiprocessing
from subprocess import call
import pdfx

# Gobal DIR 
# "Change to according to your directory"

txt_path = "./data/text/"
ref_path = "./data/references/"
pdf_path = "./data/pdf/"
have = set(os.listdir(txt_path))

def pdf_dir():
    print("In pdf_DIR")
    data = []
    for paths, dirs, file in os.walk(pdf_path):
        for f in file:
            data.append((paths, f))
    return data
 
def pdf_extract(dirs):
    print("extracting")
    '''Function takes filename and path to the file as a tuple and save the extracted text and references \
    from PDF file to txt_path dirs = ("pdf_data/", "filename.pdf")'''
    paths, filename = dirs
    file_ = filename.replace(".pdf", ".txt")
    file_json = filename.replace(".pdf", ".json")
    if file_ in have:
        print("file already extracted!!")
    else:
        print("read pdf file", filename)
        cmd_text_extractor = "pdfx %s -t -o %s" % (
            os.path.join(paths, filename), txt_path+file_)
        pdf = pdfx.PDFx(os.path.join(paths, filename))
        references_dict = pdf.get_references_as_dict()
        print("extrated reference of:", file_)
        os.system(cmd_text_extractor)
        print("extracted pdf_file:", file_)
        with open(ref_path+file_json, 'w') as fp:
            json.dump(references_dict, fp)
        print("save json to reference:", file_json)
        time.sleep(0.01)

def pdf_text_extractor():
    print("Testning")
    filenames = pdf_dir()
    filenames = filenames
    try:
        pool = multiprocessing.Pool()
        pool.map(pdf_extract, filenames)
        pool.close()
        pool.join()
    except:
        pass
