import subprocess
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import queue
from datetime import datetime, timedelta

X_s = []
X_a = []
X_v = []
X_p = []
X_raw_a = []
X_damping = []


def main():
    with subprocess.Popen(
        [
            "nios2-terminal"
        ],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    ) as process:
        
        # variables name
        # x_filt : filtered acceleration
        # x_v : velocity (area of acceleration)
        # x_p : position

        delta_t = 1e-3 # 100 microseconds
        damp = 0.005

        num_samples = 0

        x_v = 0
        x_p = 0
        x_a_prev = 0
        x_v_prev = 0
        x_damping = 0

        
        # moving average
        AVG_SIZE = 20
        x_vals = queue.Queue(AVG_SIZE)

        end_t = time.time()
        start_time = datetime.now()
        
        while True:

            result = process.stdout.readline().decode("utf-8").strip()
            accs = result.split(",")
            
            try:
                X_raw_a.append(int(accs[0]))
                x_filt = int(accs[0]) >> 1 # chop off bottom 2 bits

                # FILTERING
                # compute moving average
                if x_vals.full(): # remove extra vals
                    x_vals.get()
                x_vals.put(x_filt) # add new value

                # x_filt = 0
                # # print(list(x_vals.queue))
                for i, val in enumerate(list(x_vals.queue)):
                    x_filt += val 
                x_filt /= AVG_SIZE

                # DAMPING
                x_damping = 0
                # COMPUTING INTEGRAL

                if abs(x_filt) >= 2: 
                    if (num_samples != 0):
                        # compute area with rectangle + triangle
                        x_v += (x_a_prev * delta_t) + ((x_filt - x_a_prev) / 2) * delta_t 
                else:
                    x_damping = x_v * damp
                    x_v -= x_damping

                # compute area of velocity with rectangle + triangle
                if (num_samples != 0):
                    x_p += x_v_prev * (delta_t) + ((x_v - x_v_prev) / 2) * delta_t
                
                x_a_prev = x_filt
                x_v_prev = x_v


                # PRINT STUFF

                X_s.append(num_samples * delta_t)  
                X_a.append(x_filt)
                X_v.append(x_v)
                X_p.append(x_p)
                X_damping.append(x_damping)

                print(f'{x_filt:.2f}, {x_v:.2f}, {x_p:.2f}')    
                num_samples += 1 

            except:
                print("no data yet")

            # end_t = time.time()
            # star_t = time.time()
        

# coeffs = [-0.0117,    0.0018,    0.0017,    0.0016,    0.0015,    0.0014,    0.0014,    0.0013,    0.0013,    0.0013,    0.0012,    0.0012,    0.0012,    0.0011,    0.0011,    0.0010,    0.0009,    0.0009,    0.0008,    0.0007,    0.0006,    0.0005,    0.0003,    0.0002,    0.0001,   -0.0001,   -0.0003,   -0.0004,   -0.0006,   -0.0008,   -0.0010,   -0.0011,   -0.0013,   -0.0015,   -0.0016,   -0.0018,   -0.0019,   -0.0021,   -0.0022,   -0.0023,   -0.0023,   -0.0024,   -0.0024,   -0.0024,   -0.0023,   -0.0022,   -0.0021,   -0.0020,   -0.0018,   -0.0016,   -0.0014,   -0.0011,   -0.0008,   -0.0005,   -0.0002,    0.0002,    0.0006,    0.0010,    0.0014,    0.0018,    0.0022,    0.0027,    0.0031,    0.0035,    0.0039,    0.0043,    0.0046,    0.0049,    0.0052,    0.0054,    0.0056,    0.0057,    0.0058,    0.0058,    0.0058,    0.0057,    0.0055,    0.0052,    0.0048,    0.0044,    0.0039,    0.0033,    0.0026,    0.0019,    0.0010,    0.0001,   -0.0009,   -0.0019,   -0.0030,   -0.0042,   -0.0055,   -0.0068,   -0.0081,   -0.0095,   -0.0108,   -0.0123,   -0.0137,   -0.0151,   -0.0166,   -0.0180,   -0.0194,   -0.0207,   -0.0221,   -0.0233,   -0.0246,   -0.0257,   -0.0268,   -0.0278,   -0.0287,   -0.0295,   -0.0303,   -0.0309,   -0.0314,   -0.0318,   -0.0321,   -0.0323,    0.9677,   -0.0323,   -0.0321,   -0.0318,   -0.0314,   -0.0309,   -0.0303,   -0.0295,   -0.0287,   -0.0278,   -0.0268,   -0.0257,   -0.0246,   -0.0233,   -0.0221,   -0.0207,   -0.0194,   -0.0180,   -0.0166,   -0.0151,   -0.0137,   -0.0123,   -0.0108,   -0.0095,   -0.0081,   -0.0068,   -0.0055,   -0.0042,   -0.0030,   -0.0019,   -0.0009,    0.0001,    0.0010,    0.0019,    0.0026,    0.0033,    0.0039,    0.0044,    0.0048,    0.0052,    0.0055,    0.0057,    0.0058,    0.0058,    0.0058,    0.0057,    0.0056,    0.0054,    0.0052,    0.0049,    0.0046,    0.0043,    0.0039,    0.0035,    0.0031,    0.0027,    0.0022,    0.0018,    0.0014,    0.0010,    0.0006,    0.0002,   -0.0002,   -0.0005,   -0.0008,   -0.0011,   -0.0014,   -0.0016,   -0.0018,   -0.0020,   -0.0021,   -0.0022,   -0.0023,   -0.0024,   -0.0024,   -0.0024,   -0.0023,   -0.0023,   -0.0022,   -0.0021,   -0.0019,   -0.0018,   -0.0016,   -0.0015,   -0.0013,   -0.0011,   -0.0010,   -0.0008,   -0.0006,   -0.0004,   -0.0003,   -0.0001,    0.0001,    0.0002,    0.0003,    0.0005,    0.0006,    0.0007,    0.0008,    0.0009,    0.0009,    0.0010,    0.0011,    0.0011,    0.0012,    0.0012,    0.0012,    0.0013,    0.0013, 0.0013,    0.0014,    0.0014,    0.0015,    0.0016,    0.0017,    0.0018,   -0.0117]

if __name__ == '__main__':
    
    try:
        start_t = time.time()
        main()
    except KeyboardInterrupt:
        print("interrupted")
        

        fig = plt.figure()
        fig.set_size_inches(15,9)
        ax = fig.add_subplot(1,1,1)

        ax.plot(X_s, X_a, '-b', label='acceleration')
        ax.plot(X_s, X_raw_a, '-m', label='raw_accel')
        ax1 = ax.twinx()
        ax1.plot(X_s, X_damping, '-y', label='damping')
        ax1.plot(X_s, X_v, '-r', label='velocity')
        ax1.plot(X_s, X_p, '-g', label='position')

        sample_p = 1e-3
        num_samples = len(X_s)

        x_fft = np.linspace(0.0, 1.0/(2.0*sample_p), len(X_s)//2)

        y_fft = np.fft.fft(X_raw_a)

        fig2 = plt.figure()
        fig2.set_size_inches(15,9)

        fft = fig2.add_subplot(1,1,1)
        fft.plot(x_fft, np.abs(y_fft[:len(X_s)//2]))

        plt.legend()
        plt.show()

        # exit()
