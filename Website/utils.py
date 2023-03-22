import requests


API_IP = "http://127.0.0.1"
API_PORT = "8888"
API_URL = API_IP+":"+API_PORT

def getNodes():
    res = requests.get(url=API_URL+"/getNodes")
    return res.json()

def getMessages():
    res = requests.get(url=API_URL+"/getMessages")
    return res.json()["messages"]
