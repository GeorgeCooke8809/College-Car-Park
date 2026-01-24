import flask
from flask import Flask, request, redirect, url_for
from backend import connection
import datetime

app = Flask(__name__)

global data
data = connection()

@app.route("/", methods = ["GET"])
def index(): # TODO: implement select user type
    return redirect("./admin-dashboard", code=302)

@app.route("/admin-dashboard", methods = ["GET", "POST"])
def admin_dashboard():
    if flask.request.method == "GET":
        date = flask.request.args.get("date", default="None", type=str)

        if date == "None":
            today = datetime.date.today()
            date = today.strftime("%d/%m/%Y")
        else:
            date=f"{date[0:2]}/{date[2:4]}/{date[-4:]}"

        bookings = data.get_all_date_bookings(date)

        return flask.render_template("admin-dashboard.html",
                                    current_date=date,
                                    current_spaces=len(bookings),
                                    maximum_spaces=data.get_maximum_capacity(),
                                    bookings=bookings,
                                    )
    
    elif flask.request.method == "POST": # Triggered when a button is pressed
        if "backDate.x" in flask.request.form:
            date = flask.request.args.get("date", default="None", type=str)
            
            if date != "None":
                date = datetime.date.strptime(date, "%d%m%Y")
            else:
                date = datetime.date.today()

            new_date = date - datetime.timedelta(days=1)
            new_date = new_date.strftime("%d%m%Y")

            return redirect(f"./admin-dashboard?date={new_date}", code=304)
        elif "forwardDate.x" in flask.request.form:
            date = flask.request.args.get("date", default="None", type=str)
            
            if date != "None":
                date = datetime.date.strptime(date, "%d%m%Y")
            else:
                date = datetime.date.today()

            new_date = date + datetime.timedelta(days=1)
            new_date = new_date.strftime("%d%m%Y")

            return redirect(f"./admin-dashboard?date={new_date}", code=304)
        elif "submitNewSpaces" in flask.request.form:
            new_spaces = int(flask.request.form["newSpaces"])
            data.update_maximum_capacity(new_spaces)

            return redirect(url_for("admin_dashboard"))

        return "", 304

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
    
@app.route("/admin-pending", methods = ["GET", "POST"])
def pending():
    return flask.render_template("admin-pending.html",
                            requests=data.get_all_pending_requests()
                            )

if __name__ == "__main__":
    app.run(debug=True)