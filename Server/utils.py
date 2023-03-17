import tornado.web
import json
from Translator.utils import tapsToWord, getDelay
import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        timestamps = data_in["taps"]
        timestamps = [{'time':datetime.datetime.fromtimestamp(x)} for x in timestamps]
        word = tapsToWord(timestamps, delay=getDelay(timestamps))
        self.write(word)

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(status_code=204)
        self.write("ping")
