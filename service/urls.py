from flask import render_template
from ..HSsum import app


@app.route("/charaani", methods=['GET'])
def charaani():
    return render_template("login.html")


@app.route("/charaani/result", methods=['POST'])
def charaani_result():
    return render_template("top.html")
