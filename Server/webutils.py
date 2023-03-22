import tornado.web
import json
from .utils import deviceIDs

class NodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"ips":deviceIDs})