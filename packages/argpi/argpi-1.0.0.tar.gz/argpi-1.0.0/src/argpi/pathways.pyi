from .core import ArgumentDescription, Arguments, FetchType
from typing import List, Dict, Union, Any, Callable, Literal, Tuple, overload
from .exceptions import (
    ArgumentDoesNotHaveAValue,
    FetchValueTypeError,
    OrchestrationFault
)

class Definition:
    """Definition Class for Argument Data."""
    def __init__(self, factory: Union[List[Dict[str, str]], None] = None) -> None:
        """create a definition object
        
        #### parameter description
        - **`factory`**: `List[Dict[str, str]]`

          Optional data with which the arguments will be initialized.

          Example Data:

          ```python
          data = [
            {
                'name': 'initialization',
                'value': '--init',
                'short': '-i',
                'description': \"\"\"Initializes some value 
                Syntax: script --init\"\"\",
            },

            {
                'name': 'installation',
                'value': '--install',
                'short': '-ins',
                'description': None,
            },
          ]
          ```
        """
        ...
    
    def add(self, value: str, name: str, shortversion: str, description: Union[str, None] = None) -> None:
        """adds one argument to the pool
        
        #### parameter description
        - **`value`**: `str`

          main value of the argument such as `--install` or `--init` or simple `install` or `init`
        
        - **`name`**: `str`

          name of the argument.
        
        - **`shortversion`**: `str`

          short version of the argument, could be `-i` or `i` or whatever.
        
        - **`description`**: `str | None`

          Optional description of the argument.
        """
        ...
    
    def delete(self, name: str) -> None:
        """delete an argument with the given `name` from the pool if it exists."""
        ...
    
    @property
    def count(self) -> int:
        """`returns the number of arguments added in the pool currently.`"""
        ...
    
    @property
    def data(self) -> List[Dict[str, str]]:
        """`Returns the raw data.`"""
        ...
    
    @property
    def generate_help(self) -> str:
        """`returns a string with help text for the given arguments.`"""
        ...
    

class Registered:
    """`Place holder for registered EXEC types`"""
    def __init__(self, called: bool, function: Callable, *args, **kwargs) -> None:
        """create a `Registered` object where `called` is the execution status, `function` is the callable object
        and `*args` and `**kwags` are arguments to the callable object."""
        ...

class Executed:
    """Result Place holder for all executed `Registered` type objects"""
    def __init__(sef, results: Any) -> None:
        """create a `Executed` object where `results` parameter stores the result of the executed
        `Registered` object."""
        ...

class Prep:
    """Placeholder for PREP types"""
    def __init__(self, called: bool, function: Callable, *args, **kwargs) -> None:
        """create a `Prep` object where `called` is the execution status, `function` is the callable object
        and `*ags` and `**kwargs` are arguments to the callable object."""
        ...

class PathWays:
    """PathWay class for defining argument pathways"""
    def __init__(self, definition: Definition, skip: int = 1) -> None:
        """create a `PathWays` object with `Definition` (see `Definition` class for more info)"""
        ...
    
    @overload
    def register(self, argument: str, function: Callable, type: Literal['PREP', 'EXEC'], arguments: Union[Tuple[Any], None] = None) -> None:
        """`register` a function for a specific argument, with pre-defined arguments to the `Callable`
        
        `Working`: If the `argument` is in the parsed argument pool, the `function` will be called,
        using any values (*args or **kwargs) provided after the `type` parameter.

        #### parameter description
        - `argument`: `str` : The argument (value or short value) you are registering for.
        - `function`: `Callable`: The function you want to call if the argument is prensent.
        - `type`: `Literal['PREP', 'EXEC']`: If this registration is for a prep (option values) for the argument
        or main execution.
        - `*args` and `**kwargs`: The parameters you want to pass to the callable function for this registration.
        """
        ...
    
    @overload
    def register(self, argument: str, function: Callable, type: Literal['PREP', 'EXEC'], what_value_expected: Union[Literal['Single', 'Till Next', 'Till Last'], None] = None) -> None:
        """`register` a function for a specific argument, by getting some argument value from the argument pool
        
        `Working`: If the `argument` is in the parsed argument pool, the `function` will be called with the values,
        that are provided tot he `argument` by user, as parameters.

        #### parameter description
        - `argument`: `str` : The argument (value or short value) you are registering for.
        - `function`: `Callable`: The function you want to call if the argument is prensent.
        - `type`: `Literal['PREP', 'EXEC']`: If this registration is for a prep (option values) for the argument
        or main execution.
        - `what_value_expected`: `(It is a keyword argument and must be passed as a keyword=value format.)`: `Literal['Single', 'Till Next', 'Till Last']`:
        The type of values you are expecting from the argument, such as `Single` (meaing only one string will be passed after the argument and you want that as parameter),
        `Till Next` (meaning, you want to add all the strings passed after the `argument` till the next `argument` comes.) or `Till Last` (for arguments that are called at last
        and all the values after that `argument` are parameters). If you are unsure about `Till Last` and `Till Next`, just use `Till Next` and it will handle any edge cases for you.

        #### Example
        ```
        ...

        >>> function_pathway = PathWays(...)
        # let us suppose, `--init` is an argument we defined above
        # in the definition passed to `PathWays` object.

        >>> def init(*args, **kwargs) -> Any:
        ...     # do something here
        ...     pass
        # Now we defined the working of the init argument in the above
        # function

        >>> function_pathway.register('--init', init, 'EXEC', 
        ...                           what_value_expected='Single')
        # This registration will fetch a single value after the argument
        # and pass it to the `init` function we defined above.

        # For example, This is the command passed:
        # $ your-script.py --init some_value another_value
        # The above `what_value_expected` paramter will choose a `Sigle`
        # value after the `--init` and pass it to `init` function
        # Result = init(some_value) 

        >>> function_pathway.register('--init', init, 'EXEC', 
        ...                           what_value_expected='Till Next')
        # This registration will fetch all values between `--init` argument,
        # and some other argument (or if not present, till last.) and 
        # pass it to the `init` function.

        # For example, This is the command passed:
        # $ your-script.py --init value1 value2 integer1 --quick
        # `--init` and `--quick` are two arguments.
        # All the values between them will be passed as parameter to the `init`
        # function
        # Result = init(value1, value2, integer1)

        >>> function_pathway.register('--init', init, 'EXEC', 
        ...                           what_value_expected='Till Last')
        # It works in a similar way as `Till Next`, except, It is for arguments that
        # are known to be passed at last. If you are unsure, use `Till Next`,
        # If the argument indeed is the last argument, This will be implicitly invoked
        # by `Till Next`.
        ...
        ```
        """
        ...
    
    @property
    def orchestrate(self) -> None:
        """execute all possible pathways and store resutls
        
        Raises `OrchestrationFault` if any errors in code.
        """
        ...
    
    @property
    def find_orchestration_fault(self) -> Tuple[str, str]:
        """returns a tuple containing data about where orchestration fault happened.

        returns (argument, execution_type)

        argument is the argument value,  
        execution_type is either `EXEC` or `PREP`.
        """
        ...
    
    @property
    def validate(self) -> bool:
        """validate the orchestration.
        
        Returns True if success else False
        """
        ...
    
    def if_exec(self, argument: str) -> bool:
        """checks if a `argument` registration has been executed or not"""
        ...
    
    def result_of(self, argument: str, default: Union[Any, None] = None) -> Any:
        """Tries to return the result of execution(`EXEC`) of an argument, if failse, returns `default`"""
        ...
    