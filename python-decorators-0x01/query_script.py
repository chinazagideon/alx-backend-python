import os
from itertools import islice
import sys
import time
import importlib.util
# Add the current directory to Python path to find seed.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../python-generators-0x00/")

# Import the module with leading number
spec = importlib.util.spec_from_file_location("log_queries", os.path.join(os.path.dirname(__file__), "0-log_queries.py"))
log_queries_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log_queries_module)
log_queries = log_queries_module.log_queries

import seed as seed
connection = seed.connect_to_prodev()

# Get the list of tables in the database
conn = connection.cursor()

@log_queries("INFO")
def query_data(query):
    """
    Query data from the database.
    """
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            yield row
    except Exception as e:
        print(f"Error: {e}")
        raise e
    finally:
        if cursor: 
            cursor.close()
        

@log_queries("INFO")
def fetch_all_users(query):
    """
    Fetch all users from the database.
    """
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


query = "select * from user_data"
# generated_rows = query_data(query)
# for row in islice(generated_rows, 10):
    # print(row)

users = fetch_all_users(query)
for row in islice(users, 10):
    print(row)

