import sys
import argparse
import pandas as pd
import os

url_zones = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
zones_file = 'zones.csv'
zones_table_name = 'taxi_zones'

os.system(f"wget {url_zones} -O {zones_file}")
df_zone = pd.read_csv(zones_file)
print(df_zone)

if __name__ == "__main__":
    print("Arguments:", sys.argv)
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--param1')
    parser.add_argument('--param2')
    args = parser.parse_args()
    print("Parsed arguments:", args)
