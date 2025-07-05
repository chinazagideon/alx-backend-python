import seed as seed
from itertools import islice

# Lazy Pagination Generator with offset and limit
def lazy_paginate(limit=10, offset=0):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Main execution
if __name__ == "__main__":
    for user in islice(lazy_paginate(10, 0), 10):
        print(user)