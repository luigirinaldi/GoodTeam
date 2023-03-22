import tornado.web
import json
from Translator.utils import tapsToWord, getDelay
import datetime

messageQueue = []
deviceIDs = []
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        timestamps = data_in["taps"]
        timestamps = [{'time':datetime.datetime.fromtimestamp(x)} for x in timestamps]
        corrected_word, original_word, confidence = tapsToWord(timestamps, delay=getDelay(timestamps))
        sender = data_in["DeviceID"]
        recieve = data_in["RecipientID"]
        messageQueue.append({"to":recieve,"from":sender,"message":corrected_word, "original":original_word, "confidence":confidence})
        self.write(corrected_word, original_word, confidence)

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        pinger = data_in["DeviceID"]
        messages = [message for message in messageQueue if message["to"] in [-1,pinger]]
        buffer = {'messages':messages}
        if buffer['messages']:
            for message in messages:
                if not (message["to"] == -1 and message["from"] == pinger):
                    messageQueue.remove(message)
            self.set_status(status_code=200)
            self.write(buffer)
        else:
            self.set_status(status_code=206)
            self.write(buffer)

class StartupHandler(tornado.web.RequestHandler):
    def get(self):
        ip = self.request.remote_ip
        if ip not in deviceIDs:
            deviceIDs.append(ip)
            data = {"deviceID":deviceIDs.index(ip)}
            self.write(data)
        else:
            data = {"deviceID":deviceIDs.index(ip)}
            self.write(data)

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""Status: <br>
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣷⣶⣄⣀⣀<br>
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀<br>
⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⠁⣰⣿⣿⣿⡿⠿⠻⠿⣿⣿⣿⣿⣧<br>
⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠏⠀⣴⣿⣿⣿⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣇<br>
⠀⠀⠀⠀⢀⣠⣼⣿⣿⡏⠀⢠⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡀<br>
⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇<br>
⠀⠀⢰⣿⣿⡿⣿⣿⣿⡇⠀⠘⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⠁<br>
⠀⠀⣿⣿⣿⠁⣿⣿⣿⡇⠀⠀⠻⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⠃<br>
⠀⢰⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁<br>
⠀⢸⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⢉⣿⣿<br>
⠀⢸⣿⣿⣇⠀⣿⣿⣿⠀⠀⠀⠀⠀⢀⣤⣤⣤⡀⠀⠀⢸⣿⣿⣿⣷⣦⠀<br>
⠀⠀⢻⣿⣿⣶⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣦⡀⠀⠉⠉⠻⣿⣿⡇<br>
⠀⠀⠀⠛⠿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠈⠹⣿⣿⣇⣀⠀⣠⣾⣿⣿⡇<br>
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣦⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀<br>
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠛⠋⠉⠉⠁⠀<br>
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉<br>
version: MVP0.1""")
