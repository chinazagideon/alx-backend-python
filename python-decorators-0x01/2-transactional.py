import email
import importlib.util
import os
import functools

# Import the module with leading number
spec = importlib.util.spec_from_file_location(
    "with_db_connection",
    os.path.join(os.path.dirname(__file__), "1-with_db_connection.py"),
)
with_db_connection_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(with_db_connection_module)
with_db_connection = with_db_connection_module.with_db_connection

def transactional(func):
    def wrapper(*args, **kwargs):
        conn = args[0]
        try: 
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            raise e # re-raise the exception to be handled by the caller
        finally:
            conn.close()
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


# update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
print(update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com"))
