import subprocess
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import queue
from datetime import datetime, timedelta

Accel = []
Magnitude = []
Magn_filt = []
X_time = []
Taps = []

TAP_SIZE = 2
TAP_THRESH = 7

def main():
    with subprocess.Popen(
        [
            "nios2-terminal"
        ],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    ) as process:
        
        delta_t = 1e-3 # 100 microseconds
        damp = 0.005

        num_samples = 0
        prevTap = 0

        isTapping = False
        numTaps = 0

        # moving average
        AVG_SIZE = 3
        avg_vals = queue.Queue(AVG_SIZE)

        end_t = time.time()
        start_time = datetime.now()
        
        prevResult = ""

        while True:

            result = process.stdout.readline().decode("utf-8").strip()
            
            if result != prevResult:            
                accs = result.split(",")
                # print(result)

                try:
                    a = [int(x) for x in accs]
                    Accel.append(a)

                    magn = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
                    Magnitude.append(magn)

                    # # print(f"{magn:.2f}", a)
                    # if (magn >= TAP_SIZE):
                    #     Taps.append(100)
                    #     print(datetime.now(), "normal Tap")
                    # else:
                    #     Taps.append(-TAP_SIZE)


                    # FILTERING
                    # compute moving average
                    if avg_vals.full(): # remove extra vals
                        avg_vals.get()
                    avg_vals.put(magn) # add new value

                    filt_magn = 0
                    # # print(list(x_vals.queue))
                    for i, val in enumerate(list(avg_vals.queue)):
                        filt_magn += val 
                    filt_magn /= AVG_SIZE

                    

                    if isTapping:
                        numTaps += 1
                        Taps.append(40)
                        # picks up the moment the signal goes from above to below the threshold ( falling edge )
                        if (prevTap >= TAP_THRESH and filt_magn < TAP_THRESH):
                            isTapping = False
                            if numTaps >= TAP_SIZE:
                                print(datetime.now(), "Tap!", numTaps)
                    else:
                        Taps.append(TAP_THRESH)
                        # picks up Rising edge
                        if ( filt_magn >= TAP_THRESH and prevTap < TAP_THRESH):
                            print("Start tapping")
                            isTapping = True
                            numTaps = 0


                    prevTap = filt_magn

                    Magn_filt.append(filt_magn)
                    
                    X_time.append(num_samples * delta_t)

                    num_samples += 1

                except:
                    print("no data yet")
            
            prevResult = result
                
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

        # ax.plot(X_time, [pt[0] for pt in Accel], label='x')
        # ax.plot(X_time, [pt[1] for pt in Accel], label='y')
        # ax.plot(X_time, [pt[2] for pt in Accel], label='z')


        # ax.plot(X_time, Magnitude, '-', label='magnitude')
        ax.plot(X_time, Magn_filt, '-m', label='magnitude filt')

        ax.plot(X_time, Taps, '-', label="Taps")
        # ax1 = ax.twinx()
        # ax1.plot(X_s, X_damping, '-y', label='damping')
        # ax1.plot(X_s, X_v, '-r', label='velocity')
        # ax1.plot(X_s, X_p, '-g', label='position')

        # sample_p = 1e-3
        # num_samples = len(X_s)

        # x_fft = np.linspace(0.0, 1.0/(2.0*sample_p), len(X_s)//2)

        # y_fft = np.fft.fft(X_raw_a)

        # fig2 = plt.figure()
        # fig2.set_size_inches(15,9)

        # fft = fig2.add_subplot(1,1,1)
        # fft.plot(x_fft, np.abs(y_fft[:len(X_s)//2]))

        plt.legend()
        plt.show()

        # exit()
