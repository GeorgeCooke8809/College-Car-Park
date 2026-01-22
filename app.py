import flask
from flask import Flask, request
from backend import connection
import datetime

# TODO: Disregard edit booking in design documents, direct users to delete and make new

app = Flask(__name__)

global data
data = connection()

@app.route("/", methods = ["GET"])
def index():
    date = flask.request.args.get("date", default="None", type=str)

    if date == "None":
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
    else:
        date=f"{date[0:2]}/{date[2:4]}/{date[-4:]}"

    print(f"{date = }")

    return flask.render_template("admin-dashboard.html",
                                 current_date = date,
                                 current_spaces = 1,
                                 maximum_spaces = 200,
                                 bookings = data.get_all_date_bookings(date)
                                 )

@app.route("/admin-dashboard", methods = ["GET", "POST"])
def admin_dashboard():
    #TODO: copy from index

    date = flask.request.args.get("date", default="None", type=str)

    if date == "None":
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
    else:
        date=f"{date[0:2]}/{date[2:4]}/{date[-4:]}"

    print(f"{date = }")

    return flask.render_template("admin-dashboard.html",
                                 current_date = date,
                                 current_spaces = 1,
                                 maximum_spaces = 200,
                                 bookings = data.get_all_date_bookings(date)
                                 )

@app.route("/admin-view-user", methods = ["GET", "POST"])
def view_user():
    userID = flask.request.args.get("uid", default="None", type=str)

    if userID == "None":
        raise Exception("ERROR: No User ID provided")
    else:
        return flask.render_template("admin-view-user.html",
                                 user_data=data.get_user_profile_data(userID),
                                 user_cars=data.get_all_user_cars(userID) 
                                 )

if __name__ == "__main__":
    app.run(debug=True)

    # TODO: test issue
    # TODO: test issue 2