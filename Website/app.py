from flask import Flask, redirect, url_for, render_template
import utils 

def create_app():
    app = Flask(__name__,template_folder='templates')
    return app

app = create_app()
@app.route("/")
def welcome():
    return render_template("index.html")
@app.route("/dashboard")
def home():
    ips = utils.getNodes()["ips"]
    print(ips)
    return render_template("dash.html", nodes = ips,len = len(ips))


app.run(debug=True)