import seed as seed

# Stream user ages
def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()

# Compute average age of users
def compute_average_age(stream_user_ages):
    total_age = 0
    count = 0
    for age in stream_user_ages:
        total_age += age
        count += 1
    return total_age / count if count > 0 else 0

print(f"Average age: {compute_average_age(stream_user_ages())}")