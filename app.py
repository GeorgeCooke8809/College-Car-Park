import flask
from flask import Flask, request
from backend import connection

app = Flask(__name__)
data = connection()

@app.route("/", methods = ["GET", "POST"])
def index():
    pass

if __name__ == "__main__":
    app.run(debug=True)