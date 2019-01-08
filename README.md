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

```mermaid
graph TD;
    Master-->|Master Parent Process 1|rss_fetcher_pdf_downloader[bulk_pdf_train_node_builder];
    rss_fetcher_pdf_downloader-->|Process for feting papers|rss[RSS fetching from arxiv.org];
    rss-->pdf_download[Downlaoding pdf of recent published papers];
    pdf_download-->meeting_point{Master Parent Process 1 is complete? }

    Master -->|Master Parent Process 2|bulk_pdf_train_node_builder;
    bulk_pdf_train_node_builder-->Downloaing_tarfile[Downloaing tarfile from s3];
    Downloaing_tarfile-->|For each tarfile on S3|downloaing_metadata[download metadata of pdf]
    downloaing_metadata-->meeting_point
    meeting_point-->Yes
    meeting_point-->No
    No-->wait[Wait for Master Parent Process 1 to complete]
    Yes-->extract[Extracting text and references from pdf]
    extract-->node[building node in knowldge graph]
    extract-->train[Traning Doc2Vec on textfiles]
    train-->relationship[Using trained model to create relationship in knowldge graph]
    node-->creating_properties[creating references properties of node in knowldge graph]
    train-->similarity[using trained model to create similarity relationship in knowldge graph]
    extract-->|Under Development tasks|keyphrase[Extracting Keyphrase from text]
    keyphrase-->creat_tag[creating tags properties of node in knowldge graph]

```

