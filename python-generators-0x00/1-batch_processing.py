from itertools import islice
import sys
import os

# Add the current directory to Python path to find seed.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import seed as seed
connection = seed.connect_to_prodev()

# Batch processing of users
def batch_processing(batch_size=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()

# Stream users in batches
def stream_users_in_batches(batch_size=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size}")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()

