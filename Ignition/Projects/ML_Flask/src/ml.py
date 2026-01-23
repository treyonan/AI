import psycopg2
import conn_params
import pandas as pd
from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def linearReg():

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

    print("Connected to db!")

    db_data = pd.read_sql_query('select * from public.heat_demand_info();', conn)

    days = []
    hours = []
    for t in db_data["datetime"]:
        days.append(t.weekday())
        hours.append(t.hour)

    inputs = {'temperature': db_data["temperature"], 'day': days, 'hour': hours}

    df_inputs = pd.DataFrame(inputs)

    X = df_inputs
    y = db_data["heat_demand"]

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # create linear regression object
    model = linear_model.LinearRegression()

    model.fit(x_train, y_train)

    y_pred_train = model.predict(x_train)
    y_pred_test = model.predict(x_test)

    y_pred_train_series = pd.Series(y_pred_train, index=y_train.index)
    y_pred_test_series = pd.Series(y_pred_test, index=y_test.index)
    y_predictions = pd.concat([y_pred_train_series, y_pred_test_series]).sort_index()

    err_train = metrics.mean_squared_error(y_train, y_pred_train)
    err_test = metrics.mean_squared_error(y_test, y_pred_test)

    '''
    # True values    
    plt.plot(db_data.index, db_data["heat_demand"], label="True Values", color="blue")

    # Predicted values
    plt.plot(y_predictions.index, y_predictions, label="Predictions", color="red")

    plt.legend()
    plt.show()
    '''

    cur = conn.cursor()
    # # Add the result in the database
    for t, r in zip(y_predictions.index, y_predictions):
        cur.execute("CALL add_heat_demand_prediction(%s, %s);", (db_data["datetime"][t], r))

    conn.commit()

    cur.close()
    conn.close()

    result = ' Done with ml'
    return result



