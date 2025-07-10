import logging
import os
import time
import mysql.connector
from datetime import datetime
log_rate = "daily"
import json
import functools

# Load the mysql config file
with open('python-decorators-0x01/config.json', 'r') as f:
    config = json.load(f)

# Connects to mysql server db
def connect_db(config):
    return mysql.connector.connect(**config)
connection = connect_db(config)


# 1. Configure the logger
# Set up a basic configuration to log messages to 'file_operations.log'
# The 'level' parameter determines the minimum severity of messages to log.
# INFO means informational messages, warnings, errors, and critical errors will be logged.
logging.basicConfig(filename="log_queries.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s\n')

# Get a logger instance
logger = logging.getLogger(__name__)

# Decorator to log queries and their execution time.
def log_queries(type):
    """
    Decorator to log queries and their execution time.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args):
            start_time = time.perf_counter_ns();
            process_query = func(args)
            end_time = time.perf_counter_ns();
            duration = end_time - start_time;
            log_content = f"[{type}]: {args}, duration: {duration}s, {datetime.now()}"
            log_filename = generate_log_filename("log_queries", "log", log_rate)
            # print(log_content)
            safe_file_write(log_filename, log_content)
            return process_query
        return wrapper
    return decorator


# Attempts to write content to a file, logging success or failure.
def safe_file_write(filename, content):
    """
    Attempts to write content to a file, logging success or failure.
    """
    try:
        with open(filename, 'a') as f:
            f.write(content)
        logger.info(f"Successfully wrote to file: {filename}")
        print(f"Content successfully written to {filename}. Check {filename} for details.")
    except IOError as e:
        logger.error(f"Error writing to file {filename}: {e}")
        print(f"An error occurred writing to {filename}. Check {filename} for details.")
    except Exception as e:
        logger.critical(f"An unexpected error occurred during file write for {filename}: {e}")
        print(f"An unexpected error occurred. Check {filename} for critical errors.")

# Attempts to read content from a file, logging success or failure.
def safe_file_read(filename):
    """
    Attempts to read content from a file, logging success or failure.
    """
    if not os.path.exists(filename):
        logger.warning(f"Attempted to read non-existent file: {filename}")
        print(f"Warning: File '{filename}' does not exist. Check {filename} for details.")
        return None

    try:
        with open(filename, 'r') as f:
            content = f.read()
        logger.info(f"Successfully read from file: {filename}")
        print(f"Content successfully read from {filename}. Check {filename} for details.")
        return content
    except IOError as e:
        logger.error(f"Error reading from file {filename}: {e}")
        print(f"An error occurred reading from {filename}. Check {filename} for details.")
        return None
    except Exception as e:
        logger.critical(f"An unexpected error occurred during file read for {filename}: {e}")
        print(f"An unexpected error occurred. Check {filename} for critical errors.")
        return None
    

# Generate a log filename with a timestamp.
def generate_log_filename(filename, extension, log_rate):
    """
    Generate a log filename with a timestamp.
    """
    
    if log_rate == "daily":
        return f"{filename}_{datetime.now().strftime('%Y%m%d')}.{extension}"
    elif log_rate == "hourly":
        return f"{filename}_{datetime.now().strftime('%Y%m%d_%H')}.{extension}"
    elif log_rate == "minutely":
        return f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M')}.{extension}"
    else:
        return f"{filename}.{extension}"