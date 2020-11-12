
import bluetooth
import json
import pandas as pd
import time
import sqlite3

# HC-05 bluetooth address
bd_addr = "98:D3:11:FC:4F:48"
port = 1

# object for recording sensor data
sensor_data = {
    'timestamp' : [],
    'flex1'     : [],
    'flex2'     : [],
    'flex3'     : [],
    'flex4'     : [],
    'pres1'     : []
}
buffer = ""

def connect_db():
    """
        Create a temporary database table to store sensor readings
        User interface will read from this tempoary database sensor values
    """
    con = sqlite3.connect('./sensor_data.db')
    cur = con.cursor()
    # con.execute("DROP TABLE IF EXISTS sensor_data;")
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp INTEGER,
                        flex1     FLOAT,
                        flex2     FLOAT,
                        flex3     FLOAT,
                        flex4     FLOAT,
                        pres1     FLOAT
                    )
                """)
    return con


def connect_bluetooth(bd_addr,  port):
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    print("---BLUETOOTH CONNECTED---")
    sock.settimeout(1.0)
    return sock


def process_buffer(db_connection):

    global sensor_data
    global buffer
    
    lb_idx = buffer.find('{')
    rb_idx = buffer.find('}')
    
    while (lb_idx != -1 and rb_idx != -1):
        if lb_idx < rb_idx:
            data = json.loads(buffer[lb_idx:rb_idx+1])

            print("-----------------")
            print(data)
            
            # record sensor data
            for k,v in data.items():
                sensor_data[k].append(v)

            # save to database
            db_connection.execute("""INSERT INTO sensor_data(timestamp, flex1, flex2, flex3, flex4, pres1)
                                     VALUES (?,?,?,?,?,?)""",\
                                 [data["timestamp"], data["flex1"], data["flex2"],
                                  data['flex3'], data['flex4'], data['pres1']])
            db_connection.commit()
            
            buffer = buffer[rb_idx+1:]
        else:
            buffer = buffer[lb_idx:]
        
        lb_idx = buffer.find('{')
        rb_idx = buffer.find('}')
    


def get_sensor_data(sock, db_connection):
    """
        Read data from arduino sensors using the given socket
    """

    global buffer
    # receive more data from bluetooth connection
    try:
        data = sock.recv(4096)
        buffer += data.decode("utf-8")
    except Exception as e:
        print(e)
    process_buffer(db_connection)



    # return correct subselection of data to Dash UI
    # df = pd.DataFrame(sensor_data)
    # if df.shape[0] > 0:
    #     df = df[(df.timestamp < max(df.timestamp)) &
    #             (df.timestamp > max(df.timestamp) - 20000)]
    
    # return df


if __name__ == "__main__":

    socket = connect_bluetooth(bd_addr, port)
    db_connection = connect_db()

    cnt = 0
    while cnt < 100000000000:
        cnt += 1
        get_sensor_data(socket, db_connection)
        
    db_connection.close()
    socket.close()