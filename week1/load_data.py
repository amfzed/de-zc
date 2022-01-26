import pandas as pd
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = str(params.port)
    db = params.db
    table = params.table
    url = params.url
    csv_name = 'temp.csv'

    os.system(f"wget {url} -O {csv_name}")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}').connect()

    df_iter = pd.read_csv(csv_name, 
                    iterator = True,
                    chunksize = 100000,
                    parse_dates=['tpep_pickup_datetime',
                                'tpep_dropoff_datetime'])
    # get the first 100k rows
    df = next(df_iter)

    # create the table cols
    df.head(0).to_sql(name=table, con=engine, if_exists='replace')
    # load the first 100k rows
    df.to_sql(name=table, con=engine, if_exists='append')

    while True:
        df = next(df_iter)
        df.to_sql(name=table, con=engine, if_exists='append')
        print('Inserted another chunk')


if __name__ == '__main__':
    # argparse stuff for running via command line
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')

    # arguments we need: user, password, host, dbname, tablename, csv path
    parser.add_argument('--user', help='postgres username')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres hostname')
    parser.add_argument('--port', help='postgres port.')
    parser.add_argument('--db', help='postgres database name')
    parser.add_argument('--table', help='database table name')
    parser.add_argument('--url', help='location of csv to ingest')

    args = parser.parse_args()
    main(args)