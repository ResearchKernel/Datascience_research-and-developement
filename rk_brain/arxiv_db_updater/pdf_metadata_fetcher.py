from datetime import datetime
import feedparser
import pandas as pd
import feedparser
import os
import time
import re
import urllib.request
import requests
import boto3
s3 = boto3.client('s3')
PDF_DIR = "../data/pdf"

# Libraries

# list of filenames
arr = []
DIR_LIST = os.listdir(PDF_DIR)
for filename in DIR_LIST:
    # Regex for spliting text and number
    filenames = re.split('(\d+)', filename)
    filenames = filenames[0:-1]            # Exclude last null value
    filenames = "/".join(filenames)        # Join filenames with /
    if filenames[0] == "/":                # if start with "/" then
        # print(filenames)
        # extract file name.
        file, file_extension = os.path.splitext(PDF_DIR+"/"+filename)
        # remove extension.
        file = file.replace(PDF_DIR, "")
        file = file.replace("/", "")
        file = file.replace(".pdf", "")
        # print(file)
        # append filename to list
        arr.append(file)
    else:
        arr.append(filenames)               # else append to list

start = time.time()

# connections
filename = 'data-engineering-service/arxivdailysync/' + \
    str(datetime.date.today()) + '_pdf.txt'
csv_filename = 'data-engineering-service/arxivdailysync/' + \
    str(datetime.date.today()) + '_pdf.csv'
path = str(datetime.date.today()) + '_pdf.txt'
bucket_name = 'arxivoverload-developement'


def extract_metadata(feed):
    '''
                Function: Extract all metadata from arxiv respose

                Input: takes api respose from arxiv, arxiv_id in our database

                Return: list of dictionaries
    '''
    global db_arxiv_id

    feed_title = feed.feed.title
    feed_upadted = feed.feed.updated
    opensearch_totalresults = feed.feed.opensearch_totalresults
    opensearch_itemsperpage = feed.feed.opensearch_itemsperpage
    opensearch_startindex = feed.feed.opensearch_startindex

    metadata_dict_list = []  # save dicts
    for entry in feed.entries:
        metadata_dict = {}  # save metadata respose into dict.
        arxiv_id = entry.id.split('/abs/')[-1]
        print("fetched id:", arxiv_id)
        published = entry.published
        title = entry.title
        author_string = entry.author
        try:
            author_string += ' (%s)' % entry.arxiv_affiliation
        except AttributeError:
            pass
        last_author = author_string

        # feedparser v5.0.1 correctly handles multiple authors, print them all
        try:
            Authors = (', ').join(author.name for author in entry.authors)
        except AttributeError:
            pass
            # get the links to the abs page and pdf for this e-print
        for link in entry.links:
            if link.rel == 'alternate':
                abs_page_link = link.href
                print(abs_page_link)
            elif link.title == 'pdf':
                # The journal reference, comments and primary_category sections live under # the arxiv namespace
                pdf_link = link.href
        try:
            journal_ref = entry.arxiv_journal_ref
        except AttributeError:
            journal_ref = 'No journal ref found'
        try:
            comment = entry.arxiv_comment
        except AttributeError:
            comment = 'No comment found'
        primary_category = entry.tags[0]['term']
        # Lets get all the categories
        all_cat = [t['term'] for t in entry.tags]
        all_categories = (', ').join(all_cat)
        # The abstract is in the <summary> element
        Abstract = entry.summary
        metadata_dict['arxiv_id'] = arxiv_id
        metadata_dict['title'] = title
        metadata_dict['abstract'] = Abstract
        metadata_dict['primary_category'] = primary_category
        metadata_dict['all_categories'] = all_categories
        metadata_dict['author'] = author_string
        metadata_dict['last_author'] = last_author
        metadata_dict['authors'] = Authors
        metadata_dict['published'] = published
        metadata_dict['journal_ref'] = journal_ref
        metadata_dict['comment'] = comment
        metadata_dict['abs_page_link'] = abs_page_link
        metadata_dict['pdf_link'] = pdf_link
        metadata_dict_list.append(metadata_dict)
    return metadata_dict_list



def pdf_main():
    apis = [
        'astro-ph', 'cond-mat', 'cs', 'econ', 'eess', 'gr-qc', 'hep-ex', 'hep-lat',
        'hep-ph', 'hep-th', 'math', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th',
        'physics', 'q-bio', 'q-fin', 'quant-ph', 'stat'
    ]
    print('found total {} records'.format(len(arr)))
    f2 = open(filename, 'w')
    f2.write(str(arr))
    end = time.time()

    base_url = 'http://export.arxiv.org/api/query?search_query='

    urls = [
        'http://export.arxiv.org/api/query?search_query={0}'.format(str(element)) for element in arr[15000:]]

    for url in urls:
        response = urllib.request.urlopen(url).read()
        response = response.decode('utf-8')
        feed = feedparser.parse(response)
        data = extract_metadata(feed)
        data = pd.DataFrame(data)
        data.to_csv(csv_filename, index=False)


    s3.upload_file(path, bucket_name, filename)
    print("Save txt file to S3:data-engineering-service/arxivdailysync/")
    s3.upload_file(path, bucket_name, csv_filename)
    print("Save csv file to S3:data-engineering-service/arxivdailysync/")
