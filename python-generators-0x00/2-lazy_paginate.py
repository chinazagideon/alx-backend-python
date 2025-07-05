import seed as seed
from itertools import islice

# Lazy Pagination Generator with offset and limit
def lazy_paginate(page_size=10, offset=0):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def paginate_users(page_size, offset):
    for user in islice(lazy_paginate(page_size, offset), page_size):
        yield user

# Main execution
if __name__ == "__main__":
    for user in islice(paginate_users(10, 0), 10):
        print(user)