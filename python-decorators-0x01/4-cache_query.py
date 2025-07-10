import importlib.util
import os
import functools
import hashlib
import time
from itertools import islice

query_cache = {}

spec = importlib.util.spec_from_file_location(
    "with_db_connection",
    os.path.join(os.path.dirname(__file__), "1-with_db_connection.py"),
)
with_db_connection_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(with_db_connection_module)
with_db_connection = with_db_connection_module.with_db_connection

def cache_query(func):
    """
    Decorator to cache the result of a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[1]
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        if query_hash in query_cache:
            return query_cache[query_hash]
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        query_cache[query_hash] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
users = fetch_users_with_cache("SELECT email, age FROM user_data")
# print(users)
print(list(islice(users, 10)))