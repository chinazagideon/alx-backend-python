import sys
import importlib.util

#THIS IMPLEMENTATION IS ADAPTED TO BATCH PROCESSING

# Import the module properly
spec = importlib.util.spec_from_file_location("batch_processing", "python-generators-0x00/1-batch_processing.py")
processing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(processing)


##### print processed users in a batch of 50
try:
    for user in processing.batch_processing(50):
        print(user)
except BrokenPipeError:
    sys.stderr.close()