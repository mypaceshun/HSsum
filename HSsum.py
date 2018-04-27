from flask import Flask
from flask import render_template
from flask import request

from service.charaani import Charaani

app = Flask(__name__)


@app.route("/")
def top():
    return render_template("top.html")


@app.route("/charaani")
def charaani():
    return render_template("login.html")


@app.route("/charaani/result", methods=['POST'])
def charaani_result():
    username = request.form["username"]
    password = request.form["password"]

    c = Charaani()
    c.login(username, password)
    username = c.displayName
    records = c.fetch_recode()

    return render_template("result.html", username=username, records=records)
