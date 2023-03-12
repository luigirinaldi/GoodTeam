import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data_in = self.request.body
        data_in = json.loads(data_in)
        self.write(str(data_in["test"]))