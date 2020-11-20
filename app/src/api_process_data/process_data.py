import pandas as pd
import pathlib
import sqlite3
import numpy as np


from scipy import signal



# lambda function to be applied to dataframes
def convert_to_frontal_angle():
    
    pass


def get_session_df():
    """
        Read from continuous stream data_store/bluetooth_data.db
        and read only the rows that pertain to this session
    """

    # get raw sensor data
    db_addr = "../data_store/bluetooth_data.db"
    DB_ADDR = pathlib.Path(__file__).resolve().parent.joinpath(db_addr).resolve()

    con = sqlite3.connect(str(DB_ADDR))
    statement = f"""SELECT * FROM sensor_data"""

    df = pd.read_sql_query(statement, con).sort_values("timestamp")

    # subselect df by timestamps provided


    # convert voltages to angles
    # df['flex1'] = (df["flex1"] - 3.9011) /  (-0.0093)
    # df['flex2'] = (df["flex2"] - 3.9173) /  (-0.0077)
    # df['flex3'] = (df["flex3"] - 4.0248) /  (-0.0049)
    # df['flex4'] = (df["flex4"] - 4.0926) /  (-0.0067)

    df['flex1'] = (df["flex1"] - 3.48) /  (-0.0170)
    df['flex2'] = (df["flex2"] - 3.62) /  (-0.0110)
    df['flex3'] = (df["flex3"] - 3.75) /  (-0.0049)
    df['flex4'] = (df["flex4"] - 4.00) /  (-0.0067)


    df_session = df['timestamp'].copy().to_frame()

    # convert to ankle angles
    frontal_angle = []
    for _, row in df[['flex1', 'flex2']].iterrows():
        flex1 = row['flex1']
        flex2 = row['flex2']

        if flex1 > flex2:
            frontal_angle.append(flex1)
        else:
            frontal_angle.append((-1.0) * flex2)

    sagittal_angle = []
    for _, row in df[['flex3', 'flex4']].iterrows():
        flex3 = row['flex3']
        flex4 = row['flex4']

        if flex3 > flex4:
            sagittal_angle.append(flex3)
        else:
            sagittal_angle.append((-1.0) * flex4)


    df_session['frontal_plane'] = frontal_angle
    df_session['sagittal_plane'] = sagittal_angle

    # relabel timestamps to start from 0
    df_session['timestamp'] = df_session['timestamp'] - min(df_session['timestamp'])

    thresholds = {
        "frontal_plane": {
            "max": df_session['frontal_plane'].max(),
            "min": df_session['frontal_plane'].min(),
        },
        "sagittal_plane": {
            "max": df_session['sagittal_plane'].max(),
            "min": df_session['sagittal_plane'].min(),
        }
    }

    return df_session, thresholds





def get_metrics_by_time(df, plane, thresholds):

    x = df['timestamp']
    y = df[plane]

    threshold_max = thresholds[plane]['max'] * 0.6
    threshold_min = thresholds[plane]['min'] * 0.6

    tot_stress = (y[y > threshold_max] - threshold_max).sum() + \
                 (y[y < threshold_min].abs() - abs(threshold_min)).sum()

    avg_stress = tot_stress / len(y)

    return tot_stress, avg_stress, y.std()

def get_metrics_by_events(df, plane, thresholds, radio_value):


    x = df['timestamp']
    y = df[plane]

    threshold_max = thresholds[plane]['max'] * 0.6
    threshold_min = thresholds[plane]['min'] * 0.6

    # find jumps and landings
    # MIN_HEIGHT = 0.2
    # PEAK_WIDTH_HEIGHT = 0.95

    # peaks, _ = signal.find_peaks(y, height = MIN_HEIGHT)
    
    # # results full contains 4 arrays: widths, width_height, start_time, end_time
    # start_times, end_times = signal.peak_widths(y,
    #                          peaks, rel_height = PEAK_WIDTH_HEIGHT)

    # cur_idx = 1
    # times = list(zip(start_times, end_times))

    # jump_times = 

    # while cur_idx < len(times) - 1:
    #     cur_idx += 1

    #     cur_time = times[cur_idx]
    #     next_time = times[cur_idx + 1]
    #     prev_time = times[cur_idx - 1]

    #     if cur_time 


    tot_stress = (y[y > threshold_max] - threshold_max).sum() + \
                 (y[y < threshold_min].abs() - abs(threshold_min)).sum()

    tot_stress *= np.random.random()

    avg_stress = tot_stress / len(y)



    return tot_stress, avg_stress, y.std() *  np.random.random()

