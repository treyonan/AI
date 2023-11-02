from flask import Flask
from flask import request

import os
import signal

import psycopg2
import conn_params
import ml

import pandas as pd
from sklearn import linear_model

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! This is a test from flask_test.py"

@app.route("/test")
def test():
    return "This is our second test function."

@app.route("/params/<param1>")
def test2(param1):
    return "Our parameter is: " + param1

@app.route("/trey")
def trey():
    return "Treys function from flask_test.py"

@app.route("/_ml")
def _ml():
    result = ml.linearReg()
    return result

@app.route("/db")
def db():
    # Connect to PostgreSQL, all the connection parameters are stored in a separate file "conn_params.py":
    conn_string = "host=" + conn_params.HOST \
                  + " port=" + conn_params.PORT \
                  + " dbname=" + conn_params.DATABASE \
                  + " user=" + conn_params.USER \
                  + " password=" + conn_params.PASSWORD

    try:
        conn = psycopg2.connect(conn_string)
        result = "Connection Successful"
    except Exception as e:
        result = "Connection Not Successful"

    db_data = pd.read_sql_query('select * from public.heat_demand_info();', conn)

    conn.close()

    return result

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def kill_server():
    os.kill(os.getpid(), signal.SIGINT)


@app.route('/shutdown')
def shutdown():
    kill_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
