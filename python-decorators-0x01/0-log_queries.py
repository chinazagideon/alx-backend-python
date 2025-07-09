import logging
import os
import time
log_filename = "log_queries.log"
import datetime

# 1. Configure the logger
# Set up a basic configuration to log messages to 'file_operations.log'
# The 'level' parameter determines the minimum severity of messages to log.
# INFO means informational messages, warnings, errors, and critical errors will be logged.
logging.basicConfig(filename='log_queries.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s\n')

# Get a logger instance
logger = logging.getLogger(__name__)

def log_queries(type):
    """
    Decorator to log queries and their execution time.
    """
    def decorator(func):
        def wrapper(args):
            start_time = time.perf_counter_ns();
            process_query = func(args)
            end_time = time.perf_counter_ns();
            duration = end_time - start_time;
            log_content = f"[{type}]: {args}, duration: {duration}s, {datetime.datetime.now()}"
            # print(log_content)
            safe_file_write(log_filename, log_content)
            return process_query
        return wrapper
    return decorator


def safe_file_write(filename, content):
    """
    Attempts to write content to a file, logging success or failure.
    """
    try:
        with open(filename, 'a') as f:
            f.write(content)
        logger.info(f"Successfully wrote to file: {filename}")
        print(f"Content successfully written to {filename}. Check {log_filename} for details.")
    except IOError as e:
        logger.error(f"Error writing to file {filename}: {e}")
        print(f"An error occurred writing to {filename}. Check {log_filename} for details.")
    except Exception as e:
        logger.critical(f"An unexpected error occurred during file write for {filename}: {e}")
        print(f"An unexpected error occurred. Check {log_filename} for critical errors.")

def safe_file_read(filename):
    """
    Attempts to read content from a file, logging success or failure.
    """
    if not os.path.exists(filename):
        logger.warning(f"Attempted to read non-existent file: {filename}")
        print(f"Warning: File '{filename}' does not exist. Check {log_filename} for details.")
        return None

    try:
        with open(filename, 'r') as f:
            content = f.read()
        logger.info(f"Successfully read from file: {filename}")
        print(f"Content successfully read from {filename}. Check {log_filename} for details.")
        return content
    except IOError as e:
        logger.error(f"Error reading from file {filename}: {e}")
        print(f"An error occurred reading from {filename}. Check {log_filename} for details.")
        return None
    except Exception as e:
        logger.critical(f"An unexpected error occurred during file read for {filename}: {e}")
        print(f"An unexpected error occurred. Check {log_filename} for critical errors.")
        return None

# --- Let's test our functions and see the logs! ---

# Scenario 1: Successful write
# safe_file_write("example_log_file.txt", "This is some test content.")

# Scenario 2: Successful read
# read_content = safe_file_read("example_log_file.txt")
# if read_content:
#     print(f"Read content: {read_content.strip()}")

# Scenario 3: Attempt to read a non-existent file
# safe_file_read("non_existent_file.txt")

# Scenario 4: Simulate a permission error (this might not work on all OS/setups directly,
# but it shows where you'd log it)
# On Linux/macOS, you might try to write to a protected directory like '/root/test.txt'
# On Windows, you might try a path that doesn't have write permissions.
# For demonstration, let's just imagine it failed.
# safe_file_write("/no_write_permission/forbidden.txt", "Secret info.")
# The error handling in `safe_file_write` would catch and log this as an `IOError`