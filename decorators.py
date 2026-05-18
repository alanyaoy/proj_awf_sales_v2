

#this file created to house your reuseable timing logic to benchmark your steps



import time
import functools
import logging


logger = logging.getLogger(__name__)

def log_execution_time(func):
    ''' Decorator to measure and log the precise execution duration of a '''

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        logger.info(f"==> Starting execution: {func.__name__}")
        start_time= time.perf_counter()

        try:
            result = func(*args,**kwargs)
            return result 
        finally:
            end_time= time.perf_counter()
            duration = end_time - start_time
            logger.info(f"==> Finished: {func.__name__} (took {duration:.2f}s)")
    
    return wrapper

