import pathlib
import sqlite3
import pandas as pd





DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("wind-data.db").resolve()

DB_SENSOR_FILE = pathlib.Path(__file__).resolve().parent.joinpath("sensor_data.db").resolve()


def get_wind_data(start, end):
    """
    Query wind data rows between two ranges
    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT Speed, SpeedError, Direction FROM Wind WHERE rowid > "{start}" AND rowid <= "{end}";'
    df = pd.read_sql_query(statement, con)
    return df


def get_sensor_data():

    con = sqlite3.connect(str(DB_SENSOR_FILE))
    statement = f"""SELECT timestamp,flex1,flex2,flex3,flex4,pres1
                    FROM sensor_data
                    ORDER BY timestamp DESC
                    LIMIT 200"""

    df = pd.read_sql_query(statement, con).sort_values("timestamp")
    return df