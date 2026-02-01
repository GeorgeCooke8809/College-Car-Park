import flask
from flask import Flask, request, redirect, url_for, send_from_directory
from backend import connection
import datetime

app = Flask(__name__)
image_upload_folder = "static/userImages"
app.config["UPLOAD_FOLDER"] = image_upload_folder

global data
data = connection()

@app.route("/", methods = ["GET"])
def index(): # TODO: implement select user type
    return redirect("./admin-dashboard", code=302)

@app.route("/admin-dashboard", methods = ["GET", "POST"])
def admin_dashboard(): # TODO: split into separate get and post functions
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

            return redirect(f"./admin-dashboard?date={new_date}", code=302)
        elif "forwardDate.x" in flask.request.form:
            date = flask.request.args.get("date", default="None", type=str)
            
            if date != "None":
                date = datetime.date.strptime(date, "%d%m%Y")
            else:
                date = datetime.date.today()

            new_date = date + datetime.timedelta(days=1)
            new_date = new_date.strftime("%d%m%Y")

            return redirect(f"./admin-dashboard?date={new_date}", code=302)
        elif "submitNewSpaces" in flask.request.form:
            new_spaces = int(flask.request.form["newSpaces"])
            data.update_maximum_capacity(new_spaces)

            return redirect(url_for("admin_dashboard"))

        return "", 304

@app.route("/admin-users", methods = ["GET"])
def users():
    return flask.render_template("admin-users.html",
                                    users=data.get_all_users()
                                    )

@app.route("/admin-view-user", methods = ["GET"])
def view_user():
    userID = flask.request.args.get("uid", default="None", type=str)

    if userID == "None":
        raise Exception("ERROR: No User ID provided")

    return flask.render_template("admin-view-user.html",
                                    userID=userID,
                                    user_data=data.get_user_profile_data(userID),
                                    user_cars=data.get_all_user_cars(userID) 
                                    )

@app.route("/admin-add-booking/<bookingType>/<referer>", methods = ["POST"]) # Triggered by the add booking button in the admin view user page
def add_booking(bookingType, referer):
    userID = flask.request.args.get("uid", default="None", type=str)

    if bookingType == "day":
        date = datetime.date.strptime(flask.request.form["startDate"], "%Y-%m-%d")
        date = date.strftime("%d/%m/%Y")

        data.add_user_booking({
            "userID":userID,
            "Booking Type": "DAY",
            "Start Date": date,
            "End Date": date
        })
    elif bookingType == "season":
        start_date = datetime.date.strptime(flask.request.form["startDate"], "%Y-%m-%d")
        start_date = start_date.strftime("%d/%m/%Y")

        end_date = datetime.date.strptime(flask.request.form["endDate"], "%Y-%m-%d")
        end_date = end_date.strftime("%d/%m/%Y")

        data.add_user_booking({
            "userID":userID,
            "Booking Type": "SEASON",
            "Start Date": start_date,
            "End Date": end_date
        })
    elif bookingType == "unlimited":
        start_date = datetime.date.strptime(flask.request.form["startDate"], "%Y-%m-%d")
        start_date = start_date.strftime("%d/%m/%Y")

        data.add_user_booking({
            "userID":userID,
            "Booking Type": "UNLIMITED",
            "Start Date": start_date,
            "End Date": None
        })
    else:
        raise Exception("ERROR - Invalid type of add bookings")


    if referer == "profile":
        return redirect(f"/admin-view-user?uid={userID}")
    elif referer == "bookings":
        return redirect(f"/admin-view-user-bookings?uid={userID}")
    else:
        return redirect(f"/admin-dashboard")
    
@app.route("/admin-delete-booking", methods = ["POST"]) # Triggered by the delete booking button in the admin view bookings page
def delete_booking():
    bookingID = flask.request.args.get("bid", default="None", type=str)
    userID = flask.request.args.get("uid", default="None", type=str)

    data.delete_booking(bookingID)
    return redirect(f"/admin-view-user-bookings?uid={userID}")

@app.route("/admin-print-booking", methods = ["POST"]) # Triggered by the print booking button in the admin view bookings page
def print_booking():
    bookingID = flask.request.args.get("bid", default="None", type=str)

    data.generate_ticket_PDF(bookingID)

    return flask.send_file("Ticket.pdf", "application/pdf", as_attachment=True, download_name="Ticket.pdf")


@app.route("/admin-edit-user", methods=["POST"]) # Triggered by the edit user button in the admin view user page
def admin_edit_user():
    userID = flask.request.args.get("uid", default="None", type=str)

    return "", 304

@app.route("/admin-add-car", methods=["POST"]) # Triggered by the add car button in the admin user profile
def admin_add_car():
    userID = flask.request.args.get("uid", default="None", type=str)

    return "", 304
    
@app.route("/admin-view-user-bookings", methods = ["GET"])
def view_user_bookings():
    userID = flask.request.args.get("uid", default="None", type=str)

    if userID == "None":
        raise Exception("ERROR: No User ID provided")
    else:
        profile_data = data.get_user_profile_data(userID)

        name = f"{profile_data["First Name"]} {profile_data["Last Name"]}"

        return flask.render_template("admin-view-user-bookings.html",
                                        userID=userID,
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