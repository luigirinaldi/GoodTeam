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

timestamps = []

try:
    nios = intel_jtag_uart.intel_jtag_uart()
except Exception as e:
    print(e)
    sys.exit(0)
  
print(nios.get_info())

SAMPLE_TIME = 0.001

SERVER_URL = "http://54.90.46.38:8888/"

isFirstMessage = True
timestamp = datetime.datetime.now()
unixtimestamp = time.mktime(timestamp.timetuple()) * 1000

time_elapsed = 0


while(True):
  time.sleep(SAMPLE_TIME)
  # print("read: ", nios.read())

  b = nios.read().decode()
  if b != '':
    time_elapsed = 0
    if ( isFirstMessage ):
        # get the initial start time
        timestamp = datetime.datetime.now() 
        isFirstMessage = False
    # print("read: ", b)
    
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

  if time_elapsed > 4:
    if len(timestamps) > 0:
      # pprint(timestamps)
      # convert to unix
      timestamps = [ datetime.datetime.timestamp(x) * 1000 for x in timestamps]
      json_data = {
          "test":"test_data",
          "taps": timestamps
      }

      try:
        response = requests.get(SERVER_URL, data = json.dumps(json_data))
        print("Sent data, received response:", response)
        pprint(json.dumps(json_data))
      except Exception:
         print("Sending data failed :(", Exception)
      time_elapsed = 0
      timestamps = [] 
      




