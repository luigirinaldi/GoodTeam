from flask import Flask, redirect, url_for, render_template
import utils 
from datetime import datetime

def create_app():
    app = Flask(__name__,template_folder='templates')
    return app

def average(string):
    return round(sum([float(i) for i in string.split(" ")])/len(string.split(" ")),2)

def getTime(epoch):
    time = datetime.fromtimestamp(epoch)
    time = time.strftime("%H:%M:%S-%m/%d/%Y")
    return time

app = create_app()
@app.route("/")
def welcome():
    return render_template("index.html")
@app.route("/dashboard")
def home():
    ips = utils.getNodes()["ips"]
    messages = utils.getMessages()
    print(ips)
    return render_template("dash.html", nodes = ips,len = len(ips), messages = messages)

app.jinja_env.globals.update(average=average, getTime = getTime)
app.run(debug=True, port=8080)