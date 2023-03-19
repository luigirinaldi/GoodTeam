import json
import matplotlib.pyplot as plt
import numpy as np
import utils
import datetime

flag = 0.5
with open("sample_data\Thexquickxbrownxfoxxjumpsxoverxthexlazyxdog_fastEnd.json","r") as f:
    file = f.read()
    data = json.loads(file)

taps = data['taps']
delays = [j-i for i, j in zip(taps[:-1], taps[1:])]
counts,bin = np.histogram(delays, bins=50, density=True)
new = []
total = 0
for val in counts:
    total = val + total
    new.append(total)
cum = [x/total for x in new]
plt.stairs(cum,bin)
counts =[x/max(counts) for x in counts]
plt.stairs(counts,bin)
for idx in range(len(cum)):
    if cum[idx]>flag and counts[idx]==0 :
        delay = bin[idx]
        print(f'delay = {delay} s')
        break
plt.axvline(x = delay+0.100, color = 'g', label = 'delay threshold')
plt.show()
timestamps = [{'time':datetime.datetime.fromtimestamp(x)} for x in taps]
word = utils.tapsToWord(timestamps,delay=delay*1000,var=100)
print(word)
