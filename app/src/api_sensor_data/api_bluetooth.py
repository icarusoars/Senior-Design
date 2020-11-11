
import bluetooth
import json
import pandas as pd

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


def connect_bluetooth():
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    sock.settimeout(5.0)
    return sock

def process_buffer(buffer):
    
    lb_idx = buffer.find('{')
    rb_idx = buffer.find('}')
    
    # both brackets are found,  one json object is fully read
    if lb_idx != -1 and rb_idx != -1:
        if lb_idx < rb_idx:
            data = json.loads(buffer[lb_idx:rb_idx+1])

            print("-----------------")
            print(data)
            
            # record sensor data
            for k,v in data.items():
                sensor_data[k].append(v)
        
        return buffer[rb_idx+1:]
    # missing one or both brackets, no json object is read fully yet
    else:
        return buffer
    


def get_sensor_data(sock):
    """
        Read data from arduino sensors using the given socket
    """
    # receive more data from bluetooth connection
    try:
        data = sock.recv(96)
        buffer += data.decode("utf-8")
        buffer = process_buffer(buffer)
    except Exception as e:
        print(e)


    # return correct subselection of data to Dash UI
    df = pd.DataFrame(sensor_data)
    
    return df
