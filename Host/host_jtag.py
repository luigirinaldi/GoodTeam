import intel_jtag_uart
import sys
import time

try:
    nios = intel_jtag_uart.intel_jtag_uart()
except Exception as e:
    print(e)
    sys.exit(0)
  
print(nios.get_info())

prevVal = 0
repeated = 0

while(True):
  time.sleep(0.01)
  # print("read: ", nios.read())

  b = nios.read().decode()
  if b != '':
    print("read: ", b)
    
    b = b.split('\n')
    for val in b:
      if val != '':
        print(val, end=";")
    print("")
