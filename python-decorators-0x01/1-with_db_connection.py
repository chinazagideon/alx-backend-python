import functools
from itertools import islice
import mysql.connector
import json

# Load the mysql config file
with open('python-decorators-0x01/config.json', 'r') as f:
    config = json.load(f)

# Decorator to connect to the database and execute a function.
def with_db_connection(func):
   """
   Decorator to connect to the database and execute a function.
   """
   @functools.wraps(func)
   def wrapper(*args, **kwargs):
      connection = connect_db(config)
      cursor = connection.cursor()
      result = func(connection, *args, **kwargs)
      cursor.close()
      connection.close()
      return result
   return wrapper

# Connect to the database.
def connect_db(config):
   """
   Connect to the database.
   """
   return mysql.connector.connect(**config)

# Get a user by their ID.
@with_db_connection 
def get_user_by_id(conn, user_id): 
   """
   Get a user by their ID.
   """
   cursor = conn.cursor()   
   cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,)) 
   return cursor.fetchone()

# print(get_user_by_id(1))