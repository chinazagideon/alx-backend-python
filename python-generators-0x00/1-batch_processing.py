from itertools import islice
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

if __name__ == "__main__":
    for user in islice(batch_processing(10), 10):
        print(user)
    for stream_user in islice(stream_users_in_batches(10), 10):
        print(stream_user)