from typing import Callable
from datetime import datetime as dt

PATH_DATA = 'probability_data'

def debugger_factory(show_args = True) -> Callable:
    """
    Debugger factory function
    """
    def debugger(func: Callable) -> Callable:
        """
        Decorator that prints arguments & runtime
        """
        def wrapper(*args, **kwargs):
            """
            Wrapper that prints arguments & runtime
            """
            if show_args:
                print(f'{func.__name__} was called with:')
                print('Positional arguments:\n', args)
                print('Keyword arguments:\n', kwargs)
            # Create a timestamp (t0) 
            t0 = dt.now()
            results = func(*args, **kwargs)
            # Print runtime and return results
            print(f'{func.__name__} ran for {dt.now() - t0}')
            return results
        return wrapper
    return debugger
