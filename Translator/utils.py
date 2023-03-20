from random import random
from pprint import pprint
import datetime
import matplotlib.pyplot as plt
import numpy as np
from autocorrect import * 


tapTable = [["A","B","C","D","E"],
            ["F","G","H","I","J"],
            ["L","M","N","O","P"],
            ["Q","R","S","T","U"],
            ["V","W","X","Y","Z"]]

def letterToIndex(search,table):
    #searches for an input letter in a given table and returns the tap index 
    for (y,row) in enumerate(table):
        for (x,letter) in enumerate(row):
            if search.strip().lower() == letter.lower():
                return (y+1,x+1)

def indexToTap(index,delay=100,var=0,delayFactor=2):
    #takes a tap index and generates simulated tap data with delay between each tap and random range (ms)
    taps = []
    current_time = datetime.datetime.now()
    for i in index:
        for _ in range(i):
            tap = {"table":0,"tap":1,"time":current_time}
            taps.append(tap)
            rDelay = datetime.timedelta(milliseconds=random()*var + delay) 
            current_time = current_time + rDelay
        wordDelay = datetime.timedelta(milliseconds=(delayFactor-1)*(random()*var + delay))
        current_time = current_time + wordDelay
    return taps

def plotTapGraph(taps):
    #takes tap data and plots on a graph
    data = [tap['time'] for tap in taps]
    start_time = data[0]
    data = [(tap-start_time).total_seconds()*1000 for tap in data]
    x = [1 for tap in taps]
    plt.stem(data,x, linefmt='g-')
    plt.show()
    
def wordToTaps(word,table=tapTable,delay=100,var=0,delayFactor=2):
    #takes a word and returns simulated tap data
    taps = []
    index = []
    for letter in word:
        index.extend(letterToIndex(letter,table))
    taps = indexToTap(index,delay=delay,var=var,delayFactor=delayFactor)
    return taps

def indexToLetter(y,x,table=tapTable):
    #takes an index e.g(5,2) and returns the letter from a given table
    try:
        return table[y-1][x-1]
    except:
        return "ඞ"

def splitTaps(taps,delay=100,var=0):
    #takes taps, delay and variance and splits up the taps into letters 
    split=[]
    sub=[]
    for i in range(len(taps)):
        if i == len(taps)-1:
            sub.append(i)
            split.append(sub)
            return split
        diff = (taps[i+1]['time']-taps[i]['time']).total_seconds()*1000
        if diff < delay+var:
            sub.append(taps[i])
        else:
            sub.append(taps[i])
            split.append(sub)
            sub=[]
def tapsToWord(taps, delay=100, var=0):
    #actual useful function
    word = ""
    indexList=[]
    index = []
    taps = [len(x) for x in splitTaps(taps,delay=delay,var=var)]
    for tap in taps:
        if not len(index)%2 :
            index.append(tap)
        else:
            index.append(tap)
            indexList.append(index)
            index=[]
    print(taps)
    if any(index):
        indexList.append(index)
    for l in indexList:
        try:
            letter = indexToLetter(l[0],l[1])
            word = word + letter
        except:
            word = word

    corrected_word = my_autocorrect(word)
    return corrected_word 

def getDelay(taps,threshold=0.5):
    taps = [tap['time'].timestamp() for tap in taps]
    delays = [j-i for i, j in zip(taps[:-1], taps[1:])]
    counts,bin = np.histogram(delays, bins=50, density=True)
    new = []
    total = 0
    for val in counts:
        total = val + total
        new.append(total)
    cum = [x/total for x in new]
    #plt.stairs(cum,bin)
    counts =[x/max(counts) for x in counts]
    #plt.stairs(counts,bin)
    for idx in range(len(cum)):
        if cum[idx]>threshold and counts[idx]==0 :
            delay = bin[idx]
            print(f'delay = {delay} s')
            break
    #plt.axvline(x = delay, color = 'g', label = 'delay threshold')
    #plt.show()
    return delay*1000

