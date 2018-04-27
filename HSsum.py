from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello HSsum!"

@app.route("/shun/")
def hello_shun():
    return "Hello HSsum shun!"
