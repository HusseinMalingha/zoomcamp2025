#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f'wget -O {csv_name} {url}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')


    df.to_sql(name=table_name, con=engine, if_exists='append')

    try:
        while True:
            t_start = time()

            df = next(df_iter)
            
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print("Inserted another chunk... it took %.3f seconds" % (t_end - t_start))
    except StopIteration:
        print('No more chunk insertions!')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest data from a csv file into a postgres database')

    # user
    # password
    # host
    # port
    # database
    # table name
    # url of the csv file

    parser.add_argument('--user', help='user of postgres')
    parser.add_argument('--password', type=str, default='root', help='password of postgres')
    parser.add_argument('--host', type=str, default='localhost', help='host of postgres')
    parser.add_argument('--port', type=str, default='5432', help='port of postgres')
    parser.add_argument('--db', help='database name')
    parser.add_argument('--table_name', help='table name')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()

    main(args)
