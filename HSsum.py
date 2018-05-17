from flask import Flask
from flask import render_template
from flask import request

from service.charaani import Charaani

from operator import itemgetter, attrgetter

from logging import getLogger

logger = getLogger(__name__)
logger.setLevel('DEBUG')

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
    page = int(request.form["page"])

    c = Charaani()
    c.login(username, password)
    if c.is_login() is False:
        return render_template("fail.html")
    username = c.displayName
    records = c.fetch_recode(maxpage=page)
    key_list = sorted(records.keys())
    record_list = []
    for key in key_list:
        record_list.append(records[key])
    logger.debug(records)
    return render_template("result.html", username=username, records=record_list)
