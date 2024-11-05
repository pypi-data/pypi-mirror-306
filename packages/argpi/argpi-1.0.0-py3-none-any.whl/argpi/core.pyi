from sys import argv as __args__, exit as __exit__
from enum import Enum
from functools import wraps
from typing import Union, List, Dict, Literal
from .utils import call_once

class ArgumentDescription:
    """Argument Description class
    
    Responsible for storing argument descriptions
    """
    def __init__(self) -> None:
        """create an `ArgumentDescription` object"""
        ...
    
    @call_once
    def name(self, text: str) -> 'ArgumentDescription':
        """`set name`"""
        ...
    
    @call_once
    def description(self, text: str) -> 'ArgumentDescription':
        """`set description`"""
        ...
    
    @call_once
    def shorthand(self, text: str) -> 'ArgumentDescription':
        """`set short version`"""
        ...
    
    @property
    def __name__(self) -> str:
        """`get name of the argument`"""
        ...
    
    @property
    def __description__(self) -> str:
        """get description of the argument"""
        ...
    
    @property
    def __shorthand__(self) -> str:
        """get short version of the argument"""
        ...

class FetchType(Enum):
    """`Fetch Types for Argument Fetching`"""
    SINGULAR: Literal[1]
    TILL_LAST: Literal[2]
    TILL_NEXT: Literal[3]

class Arguments:
    """`Arguments Class for parsing`"""
    def __init__(self) -> None:
        """`create an Arguments object`"""
        ...
    
    @call_once
    def __capture__(self, skip: int = 1) -> 'Arguments':
        """`Capture the Arguments`"""
        ...
    
    def __set_arguments__(self, custom_captured_arguments: List[str]) -> 'Arguments':
        """`set your own arguments`"""
        ...
    
    def __add__(self, arg: str, argument_description: ArgumentDescription) -> None:
        """`Add an argument to the pool`"""
        ...
    
    def __analyse__(self) -> None:
        """`parse`"""
        ...
    
    def __there__(self, check: str) -> bool:
        """`checks if an argument is passed.`"""
        ...
    
    def __fetch__(self, arg: str, fetch_type: FetchType) -> Union[str, List[str]]:
        """Fetches an argument based on fetch type"""
        ...
    
    def __argument_has_value__(self, arg: str) -> bool:
        """`checks if an argument has value`"""
        ...
    