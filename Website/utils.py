import requests 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import datetime



API_IP = "http://127.0.0.1"
API_PORT = "8888"
API_URL = API_IP+":"+API_PORT
tapTable = [["A","B","C","D","E"],
            ["F","G","H","I","J"],
            ["L","M","N","O","P"],
            ["Q","R","S","T","U"],
            ["V","W","X","Y","Z"]]
def getNodes():
    res = requests.get(url=API_URL+"/getNodes")
    return res.json()

def letterToIndex(search,table=tapTable):
    #searches for an input letter in a given table and returns the tap index 
    for (y,row) in enumerate(table):
        for (x,letter) in enumerate(row):
            if search.strip().lower() == letter.lower():
                return str(y+1) + "," + str(x+1) + "|"
    
def translate(words):
    words = words.lower()
    words = words.replace(" ", "x")
    words = words.replace("k", "c")
    output = ""
    for letter in words:
        output = output + letterToIndex(letter)
    return output


def getMessages():
    res = requests.get(url=API_URL+"/getMessages")
    if res:
        message = res.json()["messages"]
        message.reverse()
        message = message[:10]
        return message
    else:
        return []
    
def plotTapGraph(timestamp):
    res = requests.get(url=API_URL+"/getMessages")
    messages = res.json()["messages"]
    messages = [message for message in messages if datetime.fromtimestamp(float(message['timeKey'])).strftime("%H:%M:%S") == timestamp]
    taps = messages[0]['timestamps']
    data = [tap['time'] for tap in taps]
    start_time = data[0]
    data = [(tap-start_time).total_seconds()*1000 for tap in data]
    x = [1 for tap in taps]
    fig = Figure()
    axis = fig.subplot()
    fig = axis.stem(data,x, linefmt='g-')
    return fig