import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time

df_parq = pq.ParquetFile('yellow_tripdata_2021-01.parquet')
df_iter = df_parq.iter_batches(batch_size=100_000)
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

df = next(df_iter).to_pandas()
df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

while True:
  t1 = time()
  df.tpep_pickup_datetime  = pd.to_datetime(df.tpep_pickup_datetime)
  df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
  df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
  t2 = time()
  print("Time elapsed {:.2f} seconds".format(t2 - t1))
  try:
    df = next(df_iter).to_pandas()
  except StopIteration:
    break