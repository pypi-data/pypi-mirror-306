import os
import pickle
import logging
from functools import wraps

def check_cache(arg_name, override=False, create_dirs=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find the named argument in kwargs
            if arg_name in kwargs:
                file_name = kwargs[arg_name]
            else:
                raise ValueError(f"Argument '{arg_name}' not found in function call")

            # Create directories if needed
            if create_dirs:
                os.makedirs(os.path.dirname(file_name), exist_ok=True)

            # Check if the file exists
            if os.path.exists(file_name) and not override:
                # Load the object from the file
                with open(file_name, 'rb') as file:
                    result = pickle.load(file)
                logging.info(f"Loaded result from {file_name}")
            else:
                # Execute the function and save the output to the file
                result = func(*args, **kwargs)
                with open(file_name, 'wb') as file:
                    pickle.dump(result, file)
                logging.info(f"Saved result to {file_name}")
            return result
        return wrapper
    return decorator
