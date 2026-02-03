import psycopg2
from .db_config import HOST, PORT, DATABASE, USER, PASSWORD
import pandas as pd

# Connect to PostgreSQL, all the connection parameters are stored in a separate file "conn_params.py":
conn_string = "host=" + HOST \
              + " port=" + PORT \
              + " dbname=" + DATABASE \
              + " user=" + USER \
              + " password=" + PASSWORD

try:
    conn = psycopg2.connect(conn_string)
except Exception as e:
    print("There was a problem connecting to the database.")
    print(e)

print("Connected!")
del conn_string

db_data = pd.read_sql_query('select * from public.heat_demand_info();', conn)

conn.close()