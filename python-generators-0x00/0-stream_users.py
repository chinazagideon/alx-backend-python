from itertools import islice, chain
import seed as seed
connection = seed.connect_to_prodev()

def stream_users():
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total_users = cursor.fetchone()[0]
    print(f"Total users: {total_users}")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    for user in islice(stream_users(), 10):
        print(user)
       