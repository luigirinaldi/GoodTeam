import intel_jtag_uart
import sys
import time
import datetime
import matplotlib.pyplot
import matplotlib.dates
import json
from pprint import pprint
import requests

import utils

def saveTapsToFile(taps, filename):
  with open(f'sample_data/{filename}.json', 'w',encoding='utf-8') as f:
    json.dump(taps, f)

timestamps = []

try:
    nios = intel_jtag_uart.intel_jtag_uart()
except Exception as e:
    print(e)
    sys.exit(0)
  
print(nios.get_info())

SAMPLE_TIME = 0.001


################## CHANGE URL ####################
SERVER_URL = "http://54.90.46.38:8888/" 
SERVER_PING = SERVER_URL+"ping"
SERVER_START = SERVER_URL+"start"
SERVER_STATUS = SERVER_URL+"status" 
##################################################

deviceID = 42
start_res = requests.get(url=SERVER_START)
if start_res.status_code==200:
   deviceID = start_res.json()["deviceID"]
isFirstMessage = True
timestamp = datetime.datetime.now()
unixtimestamp = time.mktime(timestamp.timetuple()) * 1000

time_elapsed = 0


while(True):
  ping_data = {"DeviceID" : deviceID}
  response = requests.get(SERVER_PING, data = ping_data) # ALWAYS check server 
  time.sleep(SAMPLE_TIME)
  b = nios.read().decode()
  if b != '':
    time_elapsed = 0
    if ( isFirstMessage ):
        # get the initial start time
        timestamp = datetime.datetime.now() 
        isFirstMessage = False
    b = b.split('\n')
    for val in b:
      if val != '':
        # val is in val:time_elapsed format
        tap, timedelta = val.split(":")
        print(tap, timedelta)

        # add elapsed time
        timestamp += datetime.timedelta(milliseconds=int(timedelta))

        timestamps.append(timestamp)
  else:
    # if no message has arrived add to time 
    time_elapsed += SAMPLE_TIME

  if time_elapsed > 2: #user stop tapping
    '''
    1. Always pinging the main server at SERVER_PING using the requests library
      a. If user is sending data then stop pinging and wait for 5 seconds. 
      b. Else GET data from server --> Status: Busy 
    2. Save received data and convert to bytes 
    3. Send data to FPGA using intel.write(data)
    4. Set --> Status: Available 
    5. Go back to step 1

    check if stuff to send to server |OK|
    check if stuff to send to user   |OK|
    '''
    # Send to user
    if response.status_code == 200:
      if not response.text:  # if no data is being sent --> server finished sending
        data = requests.get(SERVER_URL).content  # assuming the data is obtained from this URL
        json_str = json.dumps(data)
        data_bytes = json_str.encode('utf-8')
        intel.write(data_bytes)  # assuming intel.write() takes bytes as input
    # Send to server 
    if len(timestamps) > 0: 
      timestamps = [ datetime.datetime.timestamp(x) for x in timestamps] # convert to unix 
      json_data = {
          "test":"test_data",
          "taps": timestamps,
          "DeviceID" : deviceID,
          "RecipientID" : -1
      }
      try:
        response = requests.get(SERVER_URL, data = json.dumps(json_data))
        print("Sent data, received response:", response)
        pprint(json.dumps(json_data))
        # Data Sent 
      except Exception:
        print("Sending data failed :(", Exception)
        time_elapsed = 0
        timestamps = []                   
    else:
      print(f'Server ping failed with status code {response.status_code}')



 
      











# import datetime
# import json
# import sys
# import time

# import matplotlib.dates
# import matplotlib.pyplot as plt
# import requests

# import intel_jtag_uart
# import utils


# def save_taps_to_file(taps, filename):
#     with open(f'sample_data/{filename}.json', 'w', encoding='utf-8') as f:
#         json.dump(taps, f)


# def get_timestamps_from_buffer(buffer):
#     timestamps = []
#     for val in buffer.split('\n'):
#         if val:
#             tap, timedelta = val.split(":")
#             print(tap, timedelta)
#             timestamp = datetime.datetime.now() + datetime.timedelta(milliseconds=int(timedelta))
#             timestamps.append(timestamp)
#     return timestamps


# def convert_timestamps_to_unix(timestamps):
#     return [datetime.datetime.timestamp(x) for x in timestamps]


# def send_data_to_fpga(intel, data):
#     data_bytes = json.dumps(data).encode('utf-8')
#     intel.write(data_bytes)


# def run():
#     try:
#         nios = intel_jtag_uart.intel_jtag_uart()
#         print(nios.get_info())
#     except Exception as e:
#         print(e)
#         sys.exit(0)

#     # Configuration
#     SERVER_URL = "http://54.90.46.38:8888/"
#     SERVER_PING = "http://54.90.46.38:8888/ping"
#     SAMPLE_TIME = 0.001

#     # State
#     buffer = ''
#     timestamps = []
#     time_elapsed = 0
#     status = 'Available'

#     while True:
#         time.sleep(SAMPLE_TIME)
#         data = nios.read().decode()

#         if data:
#             time_elapsed = 0
#             buffer += data

#             if not timestamps:
#                 timestamps = [datetime.datetime.now()]
#             timestamps +=
