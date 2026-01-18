import pyodbc
import json
import datetime

class connection:
    def __init__(self, debugging: bool = False):
         self.data = None
         self.debugging = debugging

    def connect(self):
        cs = (
                "Driver={ODBC Driver 18 for SQL Server};"
                "Server=(localdb)\\CarPark;"
                "Database=CarPark;"
                "Trusted_Connection=yes;"
            )
         
        self.debugging_statement("Connected to database...")

        return pyodbc.connect(cs)
    
    def get_all_date_bookings(self, date:str): # Date format: DD/MM/YYYY
        """
        Gets all bookings for the specified date and returns them as a 2D array.
        Array format: [[BookingID, User Name, User Status (e.g.: student)], ]
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()
                sql_date = f"{date[-4:]}{date[3:5]}{date[0:2]}"

                cursor.execute("SELECT bookingID, userID FROM dbo.Bookings WHERE (startDate <= ? AND endDate >= ?) OR (startDate <= ? AND bookingType = 'UNLIMITED')", (sql_date, sql_date, sql_date))

                to_return_IDs = cursor.fetchall()

                to_return_IDs_array = [item for item in to_return_IDs]

                to_return_array = []

                for index in to_return_IDs_array:
                    temp = [index[0]]

                    cursor.execute("SELECT fName, lName, userType FROM dbo.Users WHERE userID = ?", (index[1]))
                    user_data = cursor.fetchone()

                    temp.append(f"{user_data[0]} {user_data[1]}")
                    temp.append(user_data[2])

                    to_return_array.append(temp)

                return to_return_array                
            else:
                raise Exception("ERROR: Could not connect to database")

    def __generate_next_booking_string(self, bookingType:str, startDate:str, endDate:str=None):
        """
        Used within the library to generate the strings used to describe booking dates.
        Example output: Jan 5th 2026 - Feb 13th 2026 (Current)
        """

        self.debugging_statement(f"{bookingType = }")

        self.debugging_statement(f"{startDate = }")

        today = datetime.date.today()
        state = ""
        if startDate <= today:
            if endDate != None:
                if endDate >= today:
                    state = " (Current)"


        start_date_readable = startDate.strftime("%d/%m/%Y")
        self.debugging_statement(f"{start_date_readable = }")

        self.debugging_statement(f"{endDate = }")

        if endDate != None:
            end_date_readable = endDate.strftime("%d/%m/%Y")
            self.debugging_statement(f"{end_date_readable = }")

        if bookingType == "UNLIMITED":
            return f"Unlimited Access From {start_date_readable}{state}"
        elif bookingType == "DAY":
            if endDate >= today:
                return f"Day Pass For {start_date_readable}{state}"
            else:
                return "No Pending Bookings"
        elif bookingType == "SEASON":
            if endDate >= today:
                return f"Season Pass From {start_date_readable} to {end_date_readable}{state}"
            else:
                    return "No Pending Bookings"


    def get_all_users(self, type:list = ["STUDENT", "STAFF", "VISITOR"]):
        """
        Gets a list of all users of the system and returns them as a 2D array.
        Array format: [[userID, fName, lName, userType (e.g.: student), Next Booking String]]
        """
        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT userID, fName, lName, userType FROM dbo.Users ORDER BY fName, lName, userID ASC")

                users_temp = cursor.fetchall()
                users = []

                for user in users_temp:
                    user = [elem for elem in user]
                    today = datetime.date.today().strftime("%Y%m%d")

                    self.debugging_statement(f"{today = }")

                    cursor.execute("SELECT bookingType, startDate, endDate FROM dbo.Bookings WHERE (startDate <= ? OR endDate = Null) AND userID = ? ORDER BY startDate ASC", (today, user[0]))
                    booking_info = cursor.fetchone()

                    if booking_info != None:
                        user.append(self.__generate_next_booking_string(booking_info[0], booking_info[1], booking_info[2]))
                    else:
                        user.append("No Pending Bookings")
                    users.append(user)

                return users
            else:
                raise Exception("ERROR: Could not connect to database")

    def add_user(self, information:dict): # Dictionary IDs: First Name, Last Name, Email, Password, Phone, User Type, Image Title
        """
        Adds a user to the user table. Where value is not provided, pass None in.
        Sample information dictionary:
        {
        "First Name": "Akil",
        "Last Name": "Rameez",
        "User Type": "Student",
        "Image Title": None,
        "Email": "25cookeg899@collyers.ac.uk",
        "Password": "Password",
        "Phone": None
        }
        """
        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT userID FROM dbo.Users ORDER BY userID DESC")

                past_user_ID = cursor.fetchone()
                self.debugging_statement(f"{past_user_ID = }")

                if past_user_ID != None:
                    user_ID = int(past_user_ID[0]) + 1
                else:
                    user_ID = 1

                cursor.execute("INSERT INTO dbo.Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_ID, information["First Name"], information["Last Name"], information["User Type"], information["Image Title"], information["Email"], information["Password"], information["Phone"]))
            else:
                raise Exception("ERROR: Could not connect to database")

    def get_all_user_cars(self, userID:str):
        """
        Gets a list of all cars registered to a user.
        Array format: [[carID, Licence Plate, Make, Model, Image Path], ]
        """
        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT carID, registration, carMake, carModel, carPictureTitle FROM dbo.Cars WHERE userID = ?", (userID))

                cars = []

                for car in cursor.fetchall():
                    temp = [elem for elem in car]
                    cars.append(temp)

                return cars
            else:
                raise Exception("ERROR: Could not connect to database")

    def get_all_user_bookings(self, userID:str):
        # TODO: Implement get_all_user_bookings
        """
        Gets a list of all bookings registered to a user where the end date is after the current date.
        Array format: [[BookingID, booking date string]]
        """

    def get_next_user_booking(self, userID:str):
        all_bookings = self.get_all_user_bookings(userID)
        
        return all_bookings[0]
    
    def get_user_profile_data(self, userID:int):
        """
        Gets all the data needed to display a user's profile and outputs it as a dictionary.
        Dictionary contents: name, status (e.g.: student), image path, email, phone
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT fName, lName, userType, profilePictureTitle, email, phone FROM dbo.Users WHERE userID = ?", (userID))
                user_info = cursor.fetchone()

                return {
                    "First Name": user_info[0],
                    "Last Name": user_info[1],
                    "User Type": user_info[2],
                    "Profile Picture": user_info[3],
                    "Email": user_info[4],
                    "Phone": user_info[5],
                }
            else:
                raise Exception("ERROR: Could not connect to database")

    def edit_user(self, userID:str, updates:dict): # Dictionary IDs: Name, Email, Phone, studentType, imagePath
        # TODO: Implement edit_user
        """
        Edits any of the data included in the updates dictionary to the relevant user in the user table
        """

    def update_user_password(self, userID:str, newPassword:str):
        """
        Updates the password of the relevant user to the one provided in the users table
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("UPDATE dbo.Users SET userPassword = ? WHERE userID = ?", (newPassword, userID))
            else:
                raise Exception("ERROR: Could not connect to database")
            
    def check_user_password(self, email:str, password:str):
        """
        Checks the username and password to see if they match, returns true or false
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT userPassword from dbo.Users WHERE email = ?", (email))
                correct_password = cursor.fetchone()

                self.debugging_statement(f"{correct_password = }")

                if password == correct_password[0]:
                    return True
                else:
                    return False
            else:
                raise Exception("ERROR: Could not connect to database")

    def add_user_car(self, carDetails:dict):
        """
        Adds a car to the car table associated with the relevant user and with the details provided.
        Sample dictionary:
        {
            "userID": 1,
            "Registration": "PE14 WUA",
            "Make": "Aston Martin",
            "Model": "DB9",
            "Image Title": None
        }
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT carID FROM dbo.Cars ORDER BY carID DESC")

                past_car_ID = cursor.fetchone()
                self.debugging_statement(f"{past_car_ID = }")

                if past_car_ID != None:
                    car_ID = int(past_car_ID[0]) + 1
                else:
                    car_ID = 1

                cursor.execute("INSERT INTO dbo.Cars VALUES(?, ?, ?, ?, ?, ?)", (car_ID, carDetails["userID"], carDetails["Registration"], carDetails["Make"], carDetails["Model"], carDetails["Image Title"]))
            else:
                raise Exception("ERROR: Could not connect to database")

    def add_user_booking(self, bookingDetails:dict): # Dictionary IDs: userID, Booking Type, Start Date, End Date
        """
        Adds a booking to the bookings table with the provided details and userID

        Dictionary example:
        {
            "userID": 3,
            "Booking Type": "SEASON",
            "Start Date": "01/01/2026",
            "End Date": "14/01/2026"
        }
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT bookingID FROM dbo.Bookings ORDER BY bookingID DESC")

                past_booking_ID = cursor.fetchone()
                self.debugging_statement(f"{past_booking_ID = }")

                if past_booking_ID != None:
                    booking_ID = int(past_booking_ID[0]) + 1
                else:
                    booking_ID = 1

                start_date = bookingDetails["Start Date"]
                start_date = f"{start_date[-4:]}{start_date[3:5]}{start_date[0:2]}"
                self.debugging_statement(f"{start_date = }")

                end_date = bookingDetails["End Date"]
                if end_date != None:
                    end_date = f"{end_date[-4:]}{end_date[3:5]}{end_date[0:2]}"
                self.debugging_statement(f"{end_date = }")

                cursor.execute("INSERT INTO dbo.Bookings VALUES (?, ?, ?, ?, ?)", (booking_ID, bookingDetails["userID"], bookingDetails["Booking Type"].upper(), start_date, end_date))
            else:
                raise Exception("ERROR: Could not connect to database")

    def delete_booking(self, bookingID:str):
        # TODO: Implement delete_booking
        """
        Deletes a booking from the booking table with the provided bookingID
        """

    def generate_ticket_PDF(self, bookingID:str):
        # TODO: Implement generate_ticket_PDF
        """
        Generates a PDF that can be printed with all the relevant data about the booking provided
        """

    def get_all_pending_requests(self):
        """
        Returns a 2D array of all pending requests.
        Array Format: [[Request ID, Student Name, Student Status (e.g.: student), Date string], ]
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()
                today = datetime.date.today()
                today_sql = today.strftime("%Y%m%d")

                cursor.execute("SELECT requestID, userID, requestType, startDate, endDate FROM dbo.Requests WHERE requestStatus = 'PENDING' AND endDate >= ? ORDER BY startDate ASC", (today_sql))

                requests_temp = cursor.fetchall()

                requests = []

                for request in requests_temp:
                    cursor.execute("SELECT fName, lName, userType FROM dbo.Users WHERE userID = ?", (request[1]))
                    user_info = cursor.fetchone()

                    user_name = f"{user_info[0]} {user_info[1]}"
                    user_type = user_info[2]

                    today = datetime.date.today().strftime("%Y%m%d")

                    self.debugging_statement(f"{today = }")

                    date_string = self.__generate_next_booking_string(request[2], request[3], request[4])

                    requests.append([request[0], user_name, user_type, date_string])

                return requests
            else:
                raise Exception("ERROR: Could not connect to database")

    def approve_booking_request(self, requestID:str):
        """
        Marks the request with the relevant ID as approved and copies its data to the bookings table using self.add_user_booking
        """

        with self.connect() as connection:
            if connection is not None:
                today = datetime.date.today()

                cursor = connection.cursor()

                cursor.execute("SELECT userID, requestType, startDate, endDate FROM dbo.Requests WHERE requestID = ?", (requestID))
                request_info = cursor.fetchone()

                if request_info[3] >= today:
                    self.add_user_booking({
                                            "userID": request_info[0],
                                            "Booking Type": request_info[1],
                                            "Start Date": request_info[2].strftime("%d/%m/%Y"),
                                            "End Date": request_info[3].strftime("%d/%m/%Y")
                                        })

                    cursor.execute("UPDATE dbo.Requests SET requestStatus = 'APPROVED' WHERE requestID = ?", (requestID))
                else:
                    self.debugging_statement("WARNING: Booking already passed.")
            else:
                raise Exception("ERROR: Could not connect to database")

    def deny_booking_request(self, requestID:str):
        """
        Marks the relevant booking as denied
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("UPDATE dbo.Requests SET requestStatus = 'DENIED' WHERE requestID = ?", (requestID))
            else:
                raise Exception("ERROR: Could not connect to database")

    def request_booking(self, requestDetails:dict): # Dictionary IDs: userID, Booking Type, Start Date, End Date
        """
        Adds a booking to the requests table with the provided details and userID to be later approved

        Dictionary example:
        {
            "userID": 3,
            "Booking Type": "SEASON",
            "Start Date": "01/01/2026",
            "End Date": "14/01/2026"
        }
        """

        with self.connect() as connection:
            if connection is not None:
                cursor = connection.cursor()

                cursor.execute("SELECT requestID FROM dbo.Requests ORDER BY requestID DESC")

                past_request_ID = cursor.fetchone()
                self.debugging_statement(f"{past_request_ID = }")

                if past_request_ID != None:
                    request_ID = int(past_request_ID[0]) + 1
                else:
                    request_ID = 1

                start_date = requestDetails["Start Date"]
                start_date = f"{start_date[-4:]}{start_date[3:5]}{start_date[0:2]}"
                self.debugging_statement(f"{start_date = }")

                end_date = requestDetails["End Date"]
                if end_date != None:
                    end_date = f"{end_date[-4:]}{end_date[3:5]}{end_date[0:2]}"
                self.debugging_statement(f"{end_date = }")

                cursor.execute("INSERT INTO dbo.Requests VALUES (?, ?, ?, ?, ?, 'PENDING')", (request_ID, requestDetails["userID"], requestDetails["Booking Type"].upper(), start_date, end_date))
            else:
                raise Exception("ERROR: Could not connect to database")

    def get_maximum_capacity(self):
        """
        References adminSettings.json to find and return the maximum capacity of the car park
        """

        with open("adminSettings.json", "r") as file:
            data = json.load(file)

        self.debugging_statement(f"{data = }")

        return data["max capacity"]

    def update_maximum_capacity(self, newCapacity:int):
        """
        References adminSettings.json to update the maximum capacity of the car park
        """

        with open("adminSettings.json", "r+") as file:
            data = json.load(file)

        data["max capacity"] = newCapacity
        self.debugging_statement(f"{data = }")

        json_string = json.dumps(data, indent = 2)
        self.debugging_statement(f"{json_string = }")

        with open("adminSettings.json", "w") as file:
            file.write(json_string)
    
    def debugging_statement(self, text):
        if self.debugging:
            print(f"\033[96mDEBUGGING - {text} \033[0m")

if __name__ == "__main__":
    # Enter debugging
    debugger = connection(debugging=True)
    
    print(debugger.get_all_user_cars("2"))