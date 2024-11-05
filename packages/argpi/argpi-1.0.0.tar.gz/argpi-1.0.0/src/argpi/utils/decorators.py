from functools import wraps
from ..exceptions import OnceCallablityError

def call_once(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Use a special attribute to track if the function has been called
        if hasattr(self, '_called_functions') and func.__name__ in self._called_functions:
            raise OnceCallablityError(f"{func.__name__} can only be called once.")
        if not hasattr(self, '_called_functions'):
            self._called_functions = {}
        self._called_functions[func.__name__] = True
        return func(self, *args, **kwargs)
    return wrapper