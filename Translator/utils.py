from random import random
from pprint import pprint
import datetime
import matplotlib.pyplot as plt
import numpy as np
import re  
from collections import Counter
import textdistance 
import pandas as pd



#####################################################################
# Auto-correct 
#####################################################################
w = [] #words
with open('big.txt','r',encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

v = set(w) #vocabulary

def get_count(words):
        word_freq = {}  
        word_freq = Counter(words)
        return word_freq
word_freq = get_count(w)

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs

probs = get_probs(word_freq)

def my_autocorrect(input_word):
    input_word = input_word.lower()
    if input_word in v:
            print("Word: ",input_word.upper(), "Original word: ", input_word.upper(), "Confidence 100%, word exists: ", "1")
            return(input_word.upper(),input_word.upper(),"1")
    else:
        sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in word_freq.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index':'Word', 0:'Prob'})
        df['Similarity'] = sim
        df['Sum'] = (df['Prob'] * 1.4) + df['Similarity'] 
        output = df.sort_values(['Similarity', 'Prob', 'Sum'], ascending=False).head()
        
        best_correction = output.iat[0,0]
        confidence = output.iat[0,3]

        if (confidence < 0.3):
            print("Message: ", input_word.upper(), "Input: ",input_word.upper(), "Confidence coef too low: ",  confidence)
            return(input_word.upper(),input_word.upper(),"0")
        else:
            print("Corrected message: ", best_correction.upper(), "Original message: ", input_word.upper(), "Confidence coef: ", confidence)
            return(best_correction.upper(), input_word.upper(), str(confidence))
  
#####################################################################    
#Translator    
#####################################################################

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
    words = word.split("X")
    corrected_words = []
    original_words = []
    confidences = []
    for w in words:
        corrected_w, original_w, conf = my_autocorrect(w)
        corrected_words.append(corrected_w)
        original_words.append(original_w)
        confidences.append(conf)

    return (corrected_words, original_words, confidences)

