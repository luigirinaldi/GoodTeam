import tornado.web
import json
from .utils import deviceIDs
import sqlite3

class NodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"ips":deviceIDs})

'''
Get each message in list of dictionary object; each message is a dict obj
'''
class MessageHandler(tornado.web.RequestHandler): 
    def get(self):
        try:
            con = sqlite3.connect('mydatabase.db')
        except Error:
            print(Error)

        cursorObj = con.cursor()
        if cursorObj == {"to":0,"from":0,"message":'0', "original":'0', "confidence":'0'}:
            return 
        else:
            DB_content = con.execute('SELECT * FROM GoodDB;')
            results = DB_content.fetchall()
            self.write({"messages":[{DB_content.description[i][0]:row[i] for i in range(len(row))} for row in results]})
