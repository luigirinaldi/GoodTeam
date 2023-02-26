import subprocess
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

if __name__ == '__main__':
    with subprocess.Popen(
        [
            "nios2-terminal"
        ],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    ) as process:
        # print(stdout.decode("utf-8"))
        # for c in iter(lambda: process.stdout.read(1), b""):
        #     sys.stdout.buffer.write(c)
        plt.ion()
        fig = plt.figure()
        fig.set_size_inches(15,9)
        ax1 = fig.add_subplot(1,1,1) # span the left hand side

        max_points = 400
        points_before_update = 10

        star_t = time.time()
        end_t = time.time()

        xs = []
        y0 = []
        y1 = []
        yFFT = []
        ax1.plot(xs, y0, '-b')
        ax1.plot(xs, y1, '-r')
        counter = 0
        while True:
            # result = process.stdout.readline().decode("utf-8")
            # vals = result.split(",")
            tmp = process.stdout.read(1) # read one char
            
            try:
                while(ord(tmp) != 254): # wait for start bit
                    tmp = process.stdout.read(1)
                vals = process.stdout.read(4)
                # vals = [ord(x) for x in vals]
                # for b in vals:
                    # print(b, end=",")
                # print()
                raw = (vals[0] | ((vals[1] & 0x7f ) << 8) ) + (-(2**15) if vals[1] >> 7 == 0x1 else 0) # twos complement implementation because i don't know how to use built in python
                filt = (vals[2] | ((vals[3] & 0x7f ) << 8) ) + (-(2**15) if vals[3] >> 7 == 0x1 else 0)
                # print(raw)
                y0.append(raw)
                y1.append(filt)
                xs.append(counter)  
            except:
                print("parsing error")
                quit()

            # # print(xs[-20:])
                
            if counter % points_before_update == 0:
                ax1.clear() # the trick!!
                ax1.plot(xs[-max_points:], y0[-max_points:], '-b')
                ax1.plot(xs[-max_points:], y1[-max_points:], '-r')
                fig.canvas.draw()
                fig.canvas.flush_events()
            
            counter += 1
        
