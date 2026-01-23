import psycopg2
import pandas as pd
from sklearn import linear_model, metrics
import matplotlib.pyplot as plt
from utils.db_config import HOST, PORT, DATABASE, USER, PASSWORD


def ml():
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
    y_pred_test = pd.DataFrame(model.predict(x_test), index=range(504,696))

    y_predictions = pd.concat([y_pred_train, y_pred_test])

    err_train = metrics.mean_squared_error(y_train, y_pred_train)
    err_test = metrics.mean_squared_error(y_test, y_pred_test)

    plt.plot(db_data["heat_demand"])
    plt.plot(y_predictions)
    plt.show()

    cur = conn.cursor()
    # # Add the result in the database
    for t, r in zip(db_data["datetime"], y_predictions[0]):
        cur.execute("CALL add_heat_demand_prediction(%s, %s);", (t, r))

    conn.commit()

    cur.close()
    conn.close()


