import pandas as pd
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
  trips_table_name = params.trips_table_name
  zones_table_name = params.zones_table_name
  url_trips = params.url_trips
  url_zones = params.url_zones

  # download taxi trips and zones data
  trips_file = "trips.csv.gz"
  os.system(f"wget {url_trips} -O {trips_file}")

  zones_file = "zones.csv"
  os.system(f"wget {url_zones} -O {zones_file}")

  # load trips data in batches due to large size
  df_trips = pd.read_csv(trips_file, compression='gzip', iterator=True, chunksize=100_000)
  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

  df = next(df_trips)
  df.head(0).to_sql(name=trips_table_name, con=engine, if_exists='replace')

  while True:
    t1 = time()
    df.lpep_pickup_datetime  = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.to_sql(name=trips_table_name, con=engine, if_exists='append')
    t2 = time()
    print("Time elapsed {:.2f} seconds".format(t2 - t1))
    try:
      df = next(df_trips)
    except StopIteration:
      break

  # Zone file is small so can just upload in one go
  df_zone = pd.read_csv(zones_file)
  df_zone.to_sql(name=zones_table_name, con=engine, if_exists='replace')

if __name__ == "__main__":
  # user, password, host, port, database, URL of data
  parser = argparse.ArgumentParser(description='Ingest taxi data to Postgres')
  parser.add_argument('--user')
  parser.add_argument('--password')
  parser.add_argument('--host')
  parser.add_argument('--port')
  parser.add_argument('--database')
  parser.add_argument('--trips_table_name')
  parser.add_argument('--zones_table_name')
  parser.add_argument('--url_trips')
  parser.add_argument('--url_zones')
  args = parser.parse_args()
  main(args)