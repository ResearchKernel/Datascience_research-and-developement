# Recommendation System for Researchkernel 

At reseachkernel we are building knowldge graph storing in a graph database, we use doc2vec by gensim for getting similarity between research papers. Keyphrase Extraction for extracting key words from research papers, and summarizing researhing papers. All these extracted data will be stored into knowldge graph that can be used for multi disciplinary research.

# Project Structure 
```.
├── README.md
├── data
│   ├── daily_update
│   ├── pdf
│   ├── references
│   ├── tar
│   └── text
├── main.py
├── requirements.txt
└── rk_brain
    ├── Utils
    │   ├── __init__.py
    │   ├── clean_metadata.py
    │   └── credentials.py
    ├── __init__.py
    ├── arxiv_db_updater
    │   ├── __init__.py
    │   ├── download_pdf.py
    │   ├── get_s3.py
    │   ├── get_tarfile.py
    │   ├── pdf_metadata_fetcher.py
    │   └── rss_fetcher.py
    ├── contentbased_recsys
    │   └── scripts
    │       ├── clean_metadata.py
    │       ├── database_upload.py
    │       ├── online-tran.py
    │       ├── online_train.py
    │       └── train.py
    ├── etl
    │   ├── __init__.py
    │   └── pdftotext.py
    └── knowldgegraph
        ├── abstract
        │   ├── neo4j_node_builder_abstract.py
        │   └── neo4j_relationship_creator_abstract.py
        ├── neo4j_abstract.py
        ├── neo4j_node_builder.py
        ├── neo4j_relationship_creator.py
        └── update_neo4j.py
```


Project Structure is fairly simple and self explanatory. For understanding checkout the bellow ETL and traning graph.

# How to contribute? 



# Project Workflow Flow 

![alt text](https://mermaidjs.github.io/mermaid-live-editor/#/view/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gICAgTWFzdGVyLS0-fE1hc3RlciBQYXJlbnQgUHJvY2VzcyAxfHJzc19mZXRjaGVyX3BkZl9kb3dubG9hZGVyW0dldCBSU1NdO1xuICAgIHJzc19mZXRjaGVyX3BkZl9kb3dubG9hZGVyLS0-fFByb2Nlc3MgZm9yIGZldGluZyBwYXBlcnN8cnNzW1JTUyBmZXRjaGluZyBmcm9tIGFyeGl2Lm9yZ107XG4gICAgcnNzLS0-cGRmX2Rvd25sb2FkW0Rvd25sb2FkIHBkZiBvZiByZWNlbnQgcHVibGlzaGVkIHBhcGVyc107XG4gICAgcGRmX2Rvd25sb2FkLS0-bWVldGluZ19wb2ludHtNYXN0ZXIgUGFyZW50IFByb2Nlc3MgMSBpcyBjb21wbGV0ZT8gfVxuXG4gICAgTWFzdGVyIC0tPnxNYXN0ZXIgUGFyZW50IFByb2Nlc3MgMnxhW0dldCBQREYgdG8gUzNdO1xuICAgIGEtLT5Eb3dubG9haW5nX3RhcmZpbGVbRG93bmxvYWluZyB0YXJmaWxlIGZyb20gczNdO1xuICAgIERvd25sb2FpbmdfdGFyZmlsZS0tPnxGb3IgZWFjaCB0YXJmaWxlIG9uIFMzfGRvd25sb2FpbmdfbWV0YWRhdGFbZG93bmxvYWQgbWV0YWRhdGEgb2YgcGRmXVxuICAgIGRvd25sb2FpbmdfbWV0YWRhdGEtLT5tZWV0aW5nX3BvaW50XG4gICAgbWVldGluZ19wb2ludC0tPlllc1xuICAgIG1lZXRpbmdfcG9pbnQtLT5Ob1xuICAgIE5vLS0-d2FpdFtXYWl0IGZvciBNYXN0ZXIgUGFyZW50IFByb2Nlc3MgMSB0byBjb21wbGV0ZV1cbiAgICBZZXMtLT5leHRyYWN0W0V4dHJhY3RpbmcgdGV4dCBhbmQgcmVmZXJlbmNlcyBmcm9tIHBkZl1cbiAgICBleHRyYWN0LS0-bm9kZVtidWlsZGluZyBub2RlIGluIGtub3dsZGdlIGdyYXBoXVxuICAgIGV4dHJhY3QtLT50cmFpbltUcmFuaW5nIERvYzJWZWMgb24gdGV4dGZpbGVzXVxuICAgIHRyYWluLS0-cmVsYXRpb25zaGlwW1VzaW5nIHRyYWluZWQgbW9kZWwgdG8gY3JlYXRlIHJlbGF0aW9uc2hpcCBpbiBrbm93bGRnZSBncmFwaF1cbiAgICBub2RlLS0-Y3JlYXRpbmdfcHJvcGVydGllc1tjcmVhdGluZyByZWZlcmVuY2VzIHByb3BlcnRpZXMgb2Ygbm9kZSBpbiBrbm93bGRnZSBncmFwaF1cbiAgICB0cmFpbi0tPnNpbWlsYXJpdHlbdXNpbmcgdHJhaW5lZCBtb2RlbCB0byBjcmVhdGUgc2ltaWxhcml0eSByZWxhdGlvbnNoaXAgaW4ga25vd2xkZ2UgZ3JhcGhdXG4gICAgZXh0cmFjdC0tPnxVbmRlciBEZXZlbG9wbWVudCB0YXNrc3xrZXlwaHJhc2VbRXh0cmFjdGluZyBLZXlwaHJhc2UgZnJvbSB0ZXh0XVxuICAgIGtleXBocmFzZS0tPmNyZWF0X3RhZ1tjcmVhdGluZyB0YWdzIHByb3BlcnRpZXMgb2Ygbm9kZSBpbiBrbm93bGRnZSBncmFwaF1cbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In19)
