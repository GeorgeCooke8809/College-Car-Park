import flask
from flask import Flask, request
from backend import connection

# TODO: Disregard edit booking in design documents, direct users to delete and make new

app = Flask(__name__)
data = connection()

@app.route("/", methods = ["GET", "POST"])
def index():
    return flask.render_template("index.html",
                                 current_date = "TODAY",
                                 current_spaces = 1,
                                 maximum_spaces = 200,
                                 bookings = [[1, "George Cooke", "STUDENT"]]
                                 )

if __name__ == "__main__":
    app.run(debug=True)