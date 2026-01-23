import psycopg2
import conn_params

import pandas as pd

# Connect to PostgreSQL, all the connection parameters are stored in a separate file "conn_params.py":
conn_string = "host=" + conn_params.HOST \
              + " port=" + conn_params.PORT \
              + " dbname=" + conn_params.DATABASE \
              + " user=" + conn_params.USER \
              + " password=" + conn_params.PASSWORD

try:
    conn = psycopg2.connect(conn_string)
except Exception as e:
    print("There was a problem connecting to the database.")
    print(e)

print("Connected!")
del conn_string

db_data = pd.read_sql_query('select * from public.heat_demand_info();', conn)

conn.close()