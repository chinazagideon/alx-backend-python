# chats/middleware.py
import logging
from datetime import datetime
import time
from django.utils import timezone
import os
from django.http import HttpResponseForbidden

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

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app during certain hours of the day.
    Denies access with a 403 Forbidden error if the current server time is outside
    9 AM (09:00) and 6 PM (18:00).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = 9 #9 AM
        self.end_hour = 18 #6PM
        logging.info(f"[{datetime.now()}] RestrictAccessByTimeMiddleware initialized. Access allowed between {self.start_hour}:00 and {self.end_hour}:00.")

    def __call__(self, request):
        current_hour = datetime.now().hour

        #check current hour
        if not (self.start_hour <= current_hour < self.end_hour):
            # deny access
            logging.warning(f"[{datetime.now}] access denied path: {request.path} ")
            return HttpResponseForbidden("Access to the messaging app is restricted outside of 9 AM and 6 PM.")
        
        # proceed request if outside restricted time
        response = self.get_response(request)
        return response


        
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
