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


try:
    nios = intel_jtag_uart.intel_jtag_uart()
except Exception as e:
    print(e)
    sys.exit(0)
  
print(nios.get_info())

SAMPLE_TIME = 0.1


################## CHANGE URL ####################
SERVER_URL = "http://35.153.232.237:8888/" 
SERVER_PING = SERVER_URL + "ping" 
##################################################

timestamps = []

isFirstMessage = True
timestamp = datetime.datetime.now()
unixtimestamp = time.mktime(timestamp.timetuple()) * 1000

time_elapsed = 0

ping_json = {
  "DeviceID":5
}

while(True):
  response = requests.get(SERVER_PING, data=json.dumps(ping_json)) # ALWAYS check server 
  if response.status_code == 200:
    # if not response.text:  # if no data is being sent --> server finished sending
    #   data = requests.get(SERVER_URL).content  # assuming the data is obtained from this URL
    #   print(data)
    print(response.text)

  # time.sleep(SAMPLE_TIME)
  
  b = nios.read().decode()
  
  if b != '': # recevied a tap
    time_elapsed = 0 # reset time elapsed since new tap has been received

    if ( isFirstMessage ):
        # get the initial start time
        timestamp = datetime.datetime.now() 
        isFirstMessage = False

    b = b.split('\n') # obtain array of "tap:delay" values

    for val in b:
      if val != '': # check array value is not empty
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
    # Send to server 
    if len(timestamps) > 0: 
      timestamps = [ datetime.datetime.timestamp(x) for x in timestamps] # convert to unix 
      json_data = {
          "DeviceID":5,
          "RecipientID":5,
          "taps": timestamps
      }
      saveTapsToFile(json_data, 'Thexquickxbrownxfoxxjumpsxoverxthexlazyxdog_fastEnd')
      print("saved to file")
      try:
        response = requests.get(SERVER_URL, data =json.dumps(json_data))
        print("Sent data, received response:", response)
        pprint(json.dumps(json_data))
      except Exception:
        print("Sending data failed :(", Exception)
      
    time_elapsed = 0
    timestamps = []



 
      




