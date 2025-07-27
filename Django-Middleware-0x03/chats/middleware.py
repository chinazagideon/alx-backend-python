# chats/middleware.py
import logging
from datetime import datetime
import time
import os

# configure request logger
logger = logging.getLogger("request_logger")

# create path if it does not exist
log_path = ""
# if not os.path.exists(log_path):
# os.makedirs(log_path)

log_file_path = os.path.join(log_path, "requests.log")

# create a file handler for the logger
# logging mode "a" apend new lines to end of file
log_file_handler = logging.FileHandler(log_file_path, "a")

# define message format
formatter = logging.Formatter("%(message)s")
log_file_handler.setFormatter(formatter)

# add logger handlers, prevent multiple handlers if request is already loaded
if not logger.handlers:
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.INFO)  # set logger level


class RequestLoggingMiddleware:
    """
    Middleware to log user requests to file
    """

    def __init__(self, get_response):
        """
        Logger initialise
        """
        self.get_response = get_response
        logger.info(f"[{datetime.now()}] RequestLoggingMiddleware initialised")

    def __call__(self, request):
        """
        Execute before request
        """

        # execution start
        start_time = time.time()

        # call view
        response = self.get_response(request)

        # comletion time
        end_time = time.time()

        # duration
        exec_time = end_time - start_time

        self.process_response(request, response, exec_time)

        return response

    def process_response(self, request, response, exec_time):
        """
        Process response after view has been executed
        """

        # request user
        self.user = request.user
        logger.info("process_response log auth user")
        # log the request information
        log_message = f"{datetime.now()} - User: {self.user} - Path: {request.path}"
        # log message to file
        logger.info(log_message)

        if hasattr(request, "user") and request.user.is_authenticated:
            user_info = request.user
        else:
            user_info = "Anon"

        # log request complete
        log_reponse = f"{datetime.now()} - Execution time {exec_time:.2f} seconds, User - {user_info}"
        logger.info(log_reponse)
