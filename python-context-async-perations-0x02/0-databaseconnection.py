from contextlib import contextmanager
from itertools import islice
import mysql.connector
import json

# Load the mysql config file
with open('python-decorators-0x01/config.json', 'r') as f:
    config = json.load(f)

# Connect to the database.
def connect_db(config):
   """
   Connect to the database.
   """
   return mysql.connector.connect(**config)

# context Manager 
class DatabaseConnection:
    # initialise 
    def __init__(self, name="DBContextManager"):
        print(f'init')
        self.config = config
        self.name = name
        self.cursor = None
        self.connection = None
    def __enter__(self):
        # execute function
        print("execution stage")
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self
        except mysql.connector.Error as e:
            print (f"error: {type(e).__name__}{e}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # clean up and close connection
        print ("Execution exiting...")
        try: 
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except mysql.connector.errors.InternalError as err:
            print ("internal error")
            return False

# load data into an iteratable generator object
def generate_data(iteratable):
    for data in iteratable:
        yield data
    
      
# make datebase call using a context manager function
with DatabaseConnection() as db_connect:
    cursor = db_connect.cursor
    # cursor.execute("SELECT * FROM user_data")
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in islice(generate_data(rows), 30):
        print(f"{row}\n")