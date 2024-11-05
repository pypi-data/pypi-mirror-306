from functools import wraps
from ..exceptions import OnceCallablityError
from typing import Callable

def call_once(func: Callable):
    """`This decorator ensures the respective method can only be called once per init`"""
    ...