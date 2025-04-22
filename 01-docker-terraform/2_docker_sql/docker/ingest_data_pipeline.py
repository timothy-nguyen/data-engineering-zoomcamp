import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
  user = params.user
  password = params.password
  host = params.host
  port = params.port
  database = params.database
  table_name = params.table_name
  url = params.url

  # download taxi data
  file_name = "output.parquet"
  os.system(f"wget {url} -O {file_name}")

  df_parq = pq.ParquetFile(file_name)
  df_iter = df_parq.iter_batches(batch_size=100_000)
  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

  df = next(df_iter).to_pandas()
  df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

  while True:
    t1 = time()
    df.tpep_pickup_datetime  = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(name=table_name, con=engine, if_exists='append')
    t2 = time()
    print("Time elapsed {:.2f} seconds".format(t2 - t1))
    try:
      df = next(df_iter).to_pandas()
    except StopIteration:
      break

if __name__ == "__main__":
  # user, password, host, port, database, URL of data
  parser = argparse.ArgumentParser(description='Ingest taxi data to Postgres')
  parser.add_argument('--user')
  parser.add_argument('--password')
  parser.add_argument('--host')
  parser.add_argument('--port')
  parser.add_argument('--database')
  parser.add_argument('--table_name')
  parser.add_argument('--url')
  args = parser.parse_args()
  main(args)