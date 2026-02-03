from flask import Flask, request, jsonify
import signal
import os

import psycopg2
from utils.db_config import HOST, PORT, DATABASE, USER, PASSWORD
from models import linear_regression as lr
import pandas as pd
from sklearn import linear_model


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! This is a test"


@app.route("/test")
def test():
    return "This is our second test function."

@app.route("/foo")
def foo():
    return "This is our foo bar function."


@app.route("/params/<param1>")
def test2(param1):
    return "Our parameter is: " + param1


@app.route("/ml")
def ml(): 
    lr.ml()
    '''   
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

    db_data = pd.read_sql_query('select * from public.heat_demand_info();', conn)

    days = []
    hours = []
    for t in db_data["datetime"]:
        days.append(t.weekday())
        hours.append(t.hour)

    inputs = {'temperature': db_data["temperature"], 'day': days, 'hour': hours}

    df_inputs = pd.DataFrame(inputs)

    x_train = df_inputs.head(504)
    y_train = db_data["heat_demand"].head(504)

    x_test = df_inputs.tail(192)
    y_test = db_data["heat_demand"].tail(192)

    # create linear regression object
    model = linear_model.LinearRegression()

    model.fit(x_train, y_train)

    y_pred_train = pd.DataFrame(model.predict(x_train))
    y_pred_test = pd.DataFrame(model.predict(x_test), index=range(504, 696))

    y_predictions = pd.concat([y_pred_train, y_pred_test])

    cur = conn.cursor()
    # # Add the result in the database
    for t, r in zip(db_data["datetime"], y_predictions[0]):
        cur.execute("CALL add_heat_demand_prediction(%s, %s);", (t, r))

    conn.commit()

    cur.close()
    conn.close()
    '''
    return "Done!"


def shutdown_server():
    """Helper function for shutdown route"""
    print("Shutting down Flask server...")
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)  
    
@app.route("/shutdown", methods=["GET"])  
def shutdown():
    """Shutdown the Flask app by mimicking CTRL+C"""
    shutdown_server()
    return jsonify(success=True, message="Server shutting down..."), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0')


