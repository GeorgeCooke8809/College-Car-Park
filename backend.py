import pyodbc

class connection:
    def __init__(self):
         self.data = None

    def connect(self):
        cs = (
                "Driver={ODBC Driver 18 for SQL Server};" # The driver used for connection --> windows button search ODBC, open, drivers, copy whichever one includes "SQL"
                "Server=(localdb)\\CarPark;"
                "Database=CarPark;"
                "Trusted_Connection=yes;"
            )
         
        return pyodbc.connect(cs)
    
class debugging:
    def __init__(self):
        self.connection = connection()

if __name__ == "__main__":
    # Enter debugging
    debugger = debugging()