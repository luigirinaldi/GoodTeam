import requests


API_IP = "http://100.25.36.15"
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
    words = words.replace(" ", "X")
    words = words.replace("C", "K")
    words = words.lower()
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
    

