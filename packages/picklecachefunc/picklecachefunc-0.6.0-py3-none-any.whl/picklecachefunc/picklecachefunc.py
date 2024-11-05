import os
import pickle
import logging
from functools import wraps

def check_cache(arg_name, override=False, create_dirs=False, verbosity=logging.DEBUG):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.basicConfig(level=verbosity)

            if arg_name in kwargs:
                file_name = kwargs[arg_name]
            else:
                raise ValueError(f"Argument '{arg_name}' not found in function call")

            if create_dirs:
                os.makedirs(os.path.dirname(file_name), exist_ok=True)

            if os.path.exists(file_name) and not override:
                with open(file_name, 'rb') as file:
                    result = pickle.load(file)
                logging.debug(f"Loaded result from {file_name}")
            else:
                result = func(*args, **kwargs)
                with open(file_name, 'wb') as file:
                    pickle.dump(result, file)
                logging.debug(f"Saved result to {file_name}")
            return result
        return wrapper
    return decorator
