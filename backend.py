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
         
        self.debugging_statement("Connected to database.")

        return pyodbc.connect(cs)
    
    def get_all_date_bookings(self, date:str): # Date format: YYYY/MM/DD
        # TODO: Implement
        """
        Gets all bookings for the specified date and returns them as a 2D array.
        Array format: [[BookingID, User Name, User Status (e.g.: student)], ]
        """

    def __generate_next_booking_string(self, type:str, startDate:str, endDate:str=None):
        # TODO: Implement
        """
        Used within the library to generate the strings used to describe booking dates.
        Example output: Jan 5th 2026 - Feb 13th 2026 (Current)
        """
        return "PENDING IMPLEMENTATION"

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

                    cursor.execute(f"SELECT bookingType, startDate, endDate FROM dbo.Bookings WHERE startDate >= '{today}' ORDER BY startDate ASC")
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
        # TODO: Implement
        """
        Gets a list of all cars registered to a user.
        Array format: [[carID, Licence Plate, Make, Model, Image Path], ]
        """

    def get_all_user_bookings(self, userID:str):
        # TODO: Implement
        """
        Gets a list of all bookings registered to a user where the end date is after the current date.
        Array format: [[BookingID, booking date string]]
        """

    def get_next_user_booking(self, userID:str):
        all_bookings = self.get_all_user_bookings(userID)
        
        return all_bookings[0]
    
    def get_user_profile_data(self, userID:str):
        # TODO: Implement
        """
        Gets all the data needed to display a user's profile and outputs it as a dictionary.
        Dictionary contents: name, status (e.g.: student), image path, email, phone
        """

    def edit_user(self, userID:str, updates:dict): # Dictionary IDs: Name, Email, Phone, studentType, imagePath
        # TODO: Implement
        """
        Edits any of the data included in the updates dictionary to the relevant user in the user table
        """

    def update_user_password(self, userID:str, newPassword:str):
        # TODO: Implement
        """
        Updates the password of the relevant user to the one provided in the users table
        """

    def add_user_car(self, userID:str, carDetails:dict):
        # TODO: Implement
        """
        Adds a car to the car table associated with the relevant user and with the details provided
        """

    def add_user_booking(self, userID:str, bookingDetails:dict): # Dictionary IDs: bookingType, startDate, endDate
        # TODO: Implement
        """
        Adds a booking to the bookings table with the provided details and userID
        """

    def delete_booking(self, bookingID:str):
        # TODO: Implement
        """
        Deletes a booking from the booking table with the provided bookingID
        """

    def generate_ticket_PDF(self, bookingID:str):
        # TODO: Implement
        """
        Generates a PDF that can be printed with all the relevant data about the booking provided
        """

    def get_all_pending_requests(self):
        # TODO: Implement
        """
        Returns a 2D array of all pending requests.
        Array Format: [[Request ID, Student Name, Student Status (e.g.: student), Date string], ]
        """

    def approve_booking_request(self, requestID:str):
        # TODO: Implement
        """
        Marks the request with the relevant ID as approved and copies its data to the bookings table using self.add_user_booking
        """

    def deny_booking_request(self, requestID:str):
        # TODO: Implement
        """
        Marks the relevant booking as denied
        """

    def request_booking(self, userID:str, bookingDetails:dict): # Dictionary IDs: bookingType, startDate, endDate
        # TODO: Implement
        """
        Adds a booking to the requests table with the provided details and userID to be later approved
        """

    def get_maximum_capacity(self):
        # TODO: Implement
        """
        References adminSettings.json to find and return the maximum capacity of the car park
        """

    def update_maximum_capacity(self, newCapacity:int):
        # TODO: Implement
        """
        References adminSettings.json to update the maximum capacity of the car park
        """
    
    def debugging_statement(self, text):
        if self.debugging:
            print(f"\033[96mDEBUGGING - {text} \033[0m")

if __name__ == "__main__":
    # Enter debugging
    debugger = connection(debugging=True)
    print(debugger.get_all_users())