import tornado.web
import json
from Translator.utils import tapsToWord, getDelay
import datetime

messageQueue = []
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        timestamps = data_in["taps"]
        timestamps = [{'time':datetime.datetime.fromtimestamp(x)} for x in timestamps]
        word = tapsToWord(timestamps, delay=getDelay(timestamps))
        sender = data_in["DeviceID"]
        recieve = data_in["RecipientID"]
        messageQueue.append({"to":recieve,"from":sender,"message":word})
        self.write(word)

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        pinger = data_in["DeviceID"]
        messages = [message for message in messageQueue if message["to"] in [-1,pinger]]
        buffer = {'messages':messages}
        if buffer['messages']:
            for message in messages:
                messageQueue.remove(message)
            self.write(buffer)
            self.set_status(status_code=200)
        else:
            self.set_status(status_code=206)
            self.write(buffer)
