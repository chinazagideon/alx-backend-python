from itertools import islice
import sys
import os

# Add the current directory to Python path to find seed.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import seed as seed
connection = seed.connect_to_prodev()

def batch_processing(batch_size=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()

def stream_users_in_batches(batch_size=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size}")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()

# Example 1: Generator with early return (termination)
def batch_processing_with_early_return(batch_size=10, max_age=100):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
    try:
        for row in cursor:
            # Early return if age exceeds max_age
            if row[3] > max_age:  # Assuming age is at index 3
                return  # Stop the generator early
            yield row
    finally:
        cursor.close()
        connection.close()

# Example 2: Generator that returns a value (Python 3.3+)
def batch_processing_with_return_value(batch_size=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
    count = 0
    try:
        for row in cursor:
            yield row
            count += 1
    finally:
        cursor.close()
        connection.close()
    return count  # Return the number of processed rows

# Example 3: Generator with conditional return
def batch_processing_with_condition(batch_size=10, stop_at_email=None):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
    try:
        for row in cursor:
            yield row
            # Return early if we find a specific email
            if stop_at_email and row[2] == stop_at_email:  # Assuming email is at index 2
                return
    finally:
        cursor.close()
        connection.close()

# Example 4: Generator that returns multiple values
def batch_processing_with_stats(batch_size=10):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
    total_age = 0
    count = 0
    try:
        for row in cursor:
            yield row
            total_age += row[3]  # Assuming age is at index 3
            count += 1
    finally:
        cursor.close()
        connection.close()
    return {
        'count': count,
        'average_age': total_age / count if count > 0 else 0,
        'total_age': total_age
    }

# Example 5: Generator with return for cleanup
def batch_processing_with_cleanup(batch_size=10):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")
        for row in cursor:
            yield row
    except Exception as e:
        cursor.close()
        connection.close()
        return  # Return early on error
    finally:
        cursor.close()
        connection.close()
