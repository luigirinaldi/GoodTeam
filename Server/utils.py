import tornado.web
import json
from Translator.utils import tapsToWord
import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        timestamps = data_in["taps"]
        timestamps = [{'time':datetime.datetime.fromtimestamp(x)} for x in timestamps]
        word = tapsToWord(timestamps)
        self.write(word)
