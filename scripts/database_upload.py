import pandas as pd
import sys
import pymysql.cursors
import json
import pymysql
from sqlalchemy import create_engine
# creating engine 
engine = create_engine('mysql+pymysql://root:password123@localhost:3306/arxivOverload', echo=False)

def upload_recommended_items():
    chunk_size = 10 ** 6
    for chunk in pd.read_csv("../outputs/predections.csv", chunksize=chunk_size):
        print(chunk)
        print("loaded data")    
        table_name = "title_similarity"
        chunk.to_sql(name=table_name, con=engine, if_exists = 'append', index=False)
        print("dataframe to sql")
        print("Entries successfully uploaded to mysql server")

engine.dispose()
