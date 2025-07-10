import importlib.util
import os
import functools
import time

spec = importlib.util.spec_from_file_location(
    "with_db_connection",
    os.path.join(os.path.dirname(__file__), "1-with_db_connection.py"),
)
with_db_connection_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(with_db_connection_module)
with_db_connection = with_db_connection_module.with_db_connection

def retry_on_failure(retries=3, delay=1):
    """
    Decorator to retry a db operation on failure.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(delay)
            raise Exception("Max retries reached")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    return cursor.fetchall()

print(fetch_users_with_retry())