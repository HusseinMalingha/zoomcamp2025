#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import subprocess

from time import time

import pandas as pd
from sqlalchemy import create_engine

def download_file(url, output_file):
    try:
        # Check if URL ends with .gz
        is_gzipped = url.endswith('.gz')
        temp_file = f"{output_file}.gz" if is_gzipped else output_file
        
        # Download file using subprocess
        try:
            subprocess.run(['wget', url, '-O', temp_file], 
                         check=True,
                         capture_output=True,
                         text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"wget failed: {e.stderr}")
        
        # Extract only if gzipped
        if is_gzipped:
            try:
                subprocess.run(['gunzip', '-f', temp_file],
                             check=True,
                             capture_output=True,
                             text=True)
            except subprocess.CalledProcessError as e:
                raise Exception(f"gunzip failed: {e.stderr}")
            
    except Exception as e:
        # Cleanup temporary files
        for f in [f"{output_file}.gz", output_file]:
            if os.path.exists(f):
                os.remove(f)
        raise Exception(f"Error downloading/extracting file: {str(e)}")

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db 
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'

    try:
        download_file(url, csv_name)
    except Exception as e:
        print(f"Failed to download/extract file: {str(e)}")
        raise

    # Check if the CSV file was downloaded successfully
    if not os.path.exists(csv_name):
        raise Exception(f"Failed to download {csv_name}")
 
    # Create the connection string
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)
    
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')
    print("inserted first chunk...")

    for df in df_iter:
        t_start = time()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()
        print("inserted another chunk... took %.3f second(s)" % (t_end - t_start))
    print('Done!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to PostgreSQL')
    parser.add_argument('--user', help='Postgres user')
    parser.add_argument('--password', help='Postgres password')
    parser.add_argument('--host', help='Postgres host')
    parser.add_argument('--port', help='Postgres port')
    parser.add_argument('--db', help='Postgres database name')
    parser.add_argument('--table_name', help='Postgres table name')
    parser.add_argument('--url', help='url of CSV file to ingest')
    args = parser.parse_args()

    main(args)


# The above code reads a CSV file containing yellow taxi trip data for January 2021 in chunks of 100,000 rows at a time.
# It converts the pickup and dropoff datetime columns to datetime objects,
# and then uploads the data to a PostgreSQL database using SQLAlchemy.
# The first chunk is inserted with the 'replace' option to create the table,
# and subsequent chunks are appended to the existing table.
