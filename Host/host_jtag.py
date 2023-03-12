import intel_jtag_uart
import sys
import time
import datetime
import matplotlib.pyplot
import matplotlib.dates
from pprint import pprint

import utils

# timestamps = []
taps = []

try:
    nios = intel_jtag_uart.intel_jtag_uart()
except Exception as e:
    print(e)
    sys.exit(0)
  
print(nios.get_info())

SAMPLE_TIME = 0.001

try:
  while(True):
    time.sleep(SAMPLE_TIME)
    # print("read: ", nios.read())

    b = nios.read().decode()
    if b != '':
      # print("read: ", b)
      
      b = b.split('\n')
      timedelta = SAMPLE_TIME / (len(b) - 1)
      for val in b:
        if val != '':
          tap = {"time":datetime.datetime.now() + datetime.timedelta(seconds=timedelta), "tap":1}
          taps.append(tap)
          print(val, end=";")
      print("")
    # else:
      #  taps.append(0)
except KeyboardInterrupt:
  pprint(taps)
  print(utils.tapsToWord(taps=taps, delay=2000, var=20))
  utils.plotTapGraph(taps)

  # dates = matplotlib.dates.date2num([tap['time'] for tap in taps])
  # matplotlib.pyplot.plot_date(dates, [tap['tap'] for tap in taps], "h")
  # matplotlib.pyplot.show()
  # plot
  # plt.plot(timestamps, taps, "-o")
  # # beautify the x-labels
  # plt.gcf().autofmt_xdate()

  # plt.show()