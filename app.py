import flask
from flask import Flask, request, redirect
from backend import connection
import datetime

# TODO: Disregard edit booking in design documents, direct users to delete and make new

app = Flask(__name__)

global data
data = connection()

@app.route("/", methods = ["GET"])
def index():
    return redirect("./admin-dashboard", code=302)

@app.route("/admin-dashboard", methods = ["GET", "POST"])
def admin_dashboard():
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

@app.route("/admin-users", methods = ["GET", "POST"])
def users():
    return flask.render_template("admin-users.html",
                                    users=data.get_all_users()
                                    )

@app.route("/admin-view-user", methods = ["GET", "POST"])
def view_user():
    userID = flask.request.args.get("uid", default="None", type=str)

    if userID == "None":
        raise Exception("ERROR: No User ID provided")
    else:
        return flask.render_template("admin-view-user.html",
                                     userId=userID,
                                     user_data=data.get_user_profile_data(userID),
                                     user_cars=data.get_all_user_cars(userID) 
                                     )
    
@app.route("/admin-view-user-bookings", methods = ["GET", "POST"])
def view_user_bookings():
    userID = flask.request.args.get("uid", default="None", type=str)

    if userID == "None":
        raise Exception("ERROR: No User ID provided")
    else:
        profile_data = data.get_user_profile_data(userID)

        name = f"{profile_data["First Name"]} {profile_data["Last Name"]}"

        return flask.render_template("admin-view-user-bookings.html",
                                name = name,
                                bookings=data.get_all_user_bookings(userID)
                                )

if __name__ == "__main__":
    app.run(debug=True)