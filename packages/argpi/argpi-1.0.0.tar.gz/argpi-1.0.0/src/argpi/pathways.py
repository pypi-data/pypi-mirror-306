from .core import ArgumentDescription, Arguments, FetchType
from typing import List, Dict, Union, Any, Callable, Literal, Tuple, overload
from .exceptions import (
    ArgumentDoesNotHaveAValue,
    FetchValueTypeError,
    OrchestrationFault,
    DefinitionError,
)

class Definition:
    def __init__(self, factory: Union[List[Dict[str, str]], None] = None) -> None:
        # self.arguments: List[Dict[str, str]] = [] if factory is None else factory
        self.arguments: List[Dict[str, str]] = []
        if factory:
            for x in factory:
                if x['value'] is None:
                    raise DefinitionError("\'value\' feild missing for an argument.")
                if x['name'] is None:
                    raise DefinitionError("\'name\' feild missing for an argument.")
                if x['short'] is None:
                    raise DefinitionError("\'short\' feild missing for an argument")
                self.add(x['value'], x['name'], x['short'], x['description'] if 'description' in x else None)
    
    def add(self, value: str, name: str, shortversion: str, description: Union[str, None] = None) -> None:
        self.arguments.append(
            {
                "name": name,
                "value": value,
                "short": shortversion,
                "description": "" if description is None else description,
            }
        )
    
    def delete(self, name: str) -> None:
        for i in range(len(self.arguments)):
            if self.arguments[i]['name'] == name:
                self.arguments[i] = {}
                break
    
    @property
    def count(self) -> int:
        count = 0
        for x in self.arguments:
            if x == {}:
                continue
            else:
                count += 1
        return count
    
    @property
    def data(self) -> List[Dict[str, str]]:
        return self.arguments

    @property
    def generate_help(self) -> str:
        if len(self.arguments) == 0:
            return ""
        
        repeater = """{} ({})
        {}"""
        storage = ""
        
        for x in self.arguments:
            if x != {}:
                storage += repeater.format(x['value'], x['short'], x['description'] if x['description'] is not None else "Not enough Data.") + '\n'
        
        return storage

class Registered:
    def __init__(self, called: bool, function: Callable, *args, **kwargs) -> None:
        self.called = called
        self.function = function
        self.args = args
        self.kwargs = kwargs

class Executed:
    def __init__(self, results: Any) -> None:
        self.results = results

class Prep:
    def __init__(self, called: bool, function: Callable, *args, **kwargs) -> None:
        self.called = called
        self.function = function
        self.args = args
        self.kwargs = kwargs

class PathWays:
    def __init__(self, definition: Definition, skip: int = 1) -> None:
        self.arguments = Arguments().__capture__(skip=skip)
        
        for dictionary in definition.data:
            if dictionary != {}:
                self.arguments.__add__(
                    dictionary['value'],
                    ArgumentDescription().name(dictionary['name']).shorthand(dictionary['short']).description(dictionary['description'])
                )
            
        self.arguments.__analyse__()

        self.registered: Dict[str, Registered] = {}
        self.executed: Dict[str, Executed] = {}
        self.prep: Dict[str, List[Prep]] = {}
    
    @overload
    def register(self, argument: str, function: Callable, type: Literal['PREP', 'EXEC'], arguments: Union[Tuple[Any], None] = None) -> None: ...
    @overload
    def register(self, argument: str, function: Callable, type: Literal['PREP', 'EXEC'], what_value_expected: Literal['Single', 'Till Next', 'Till Last'] = 'Single') -> None: ...
    
    def register(self, argument: str, function: Callable, type: Literal['PREP', 'EXEC'], arguments: Union[Tuple[Any], None] = None, what_value_expected: Union[Literal['Single', 'Till Next', 'Till Last'], None] = None) -> Any:
        # Check if it is number 2 overload.
        if what_value_expected is not None:
            # It is numbe 2 overload

            # This overload handles auto placement of arguments in the function

            if not self.arguments.__argument_has_value__(argument):
                raise ArgumentDoesNotHaveAValue(f"\'{argument}\' expects atleast one value.")
            
            # If what_value_expected is Single
            if what_value_expected == 'Single':
                # If PREP, store it as prep
                if type == 'PREP':
                    prep = Prep(False, function, self.arguments.__fetch__(argument, FetchType.SINGULAR))
                    if argument not in self.prep:
                        self.prep[argument] = [prep]
                    else:
                        self.prep[argument].append(prep)
                else:
                    # Exec type Register It
                    exec_ = Registered(False, function, self.arguments.__fetch__(argument, FetchType.SINGULAR))
                    self.registered[argument] = exec_

            elif what_value_expected == 'Till Last':
                # If PREP, store it as prep
                if type == 'PREP':
                    prep = Prep(False, function, self.arguments.__fetch__(argument, FetchType.TILL_LAST))
                    if argument not in self.prep:
                        self.prep[argument] = [prep]
                    else:
                        self.prep[argument].append(prep)
                else:
                    # Exec type Register It
                    exec_ = Registered(False, function, self.arguments.__fetch__(argument, FetchType.TILL_LAST))
                    self.registered[argument] = exec_

            elif what_value_expected == 'Till Next':
                # If PREP, store it as prep
                if type == 'PREP':
                    prep = Prep(False, function, self.arguments.__fetch__(argument, FetchType.TILL_NEXT))
                    if argument not in self.prep:
                        self.prep[argument] = [prep]
                    else:
                        self.prep[argument].append(prep)
                else:
                    # Exec type Register It
                    exec_ = Registered(False, function, self.arguments.__fetch__(argument, FetchType.TILL_NEXT))
                    self.registered[argument] = exec_

            else:
                raise FetchValueTypeError(f"\'what_value_expected\' parameter can be only of the type Literal[\'Single\', \'Till Next\', \'Till Last\'], depending upon the type of fetching requires from the argument.")

        else:
            # If what_value_expected parameter is not present in args or kwargs
            # Use Overload number 1

            if type == 'PREP':
                prep = Prep(False, function, *arguments)
                if argument not in self.prep:
                    self.prep[argument] = [prep]
                else:
                    self.prep[argument].append(prep)
            else:
                exec_ = Registered(False, function, *arguments)
                self.registered[argument] = exec_
    
    @property
    def orchestrate(self) -> None:
        # Do all preps first.
        for arg, l_prep in self.prep.items():
            # do all the preps of this argument
            for i in range(len(l_prep)):
                l_prep[i].function(*l_prep[i].args, **l_prep[i].kwargs)
                l_prep[i].called = True

        # Do all executions
        for argument in self.registered:
            self.executed[argument] = Executed(self.registered[argument].function(*self.registered[argument].args, **self.registered[argument].kwargs))
            self.registered[argument].called = True
        
        if not self.validate:
            fault = self.find_orchestration_fault
            raise OrchestrationFault(f"With argument: {fault[0]}, type: {fault[1]}")
    
    @property
    def find_orchestration_fault(self) -> Tuple[str, str]:
        for argument, l_prep in self.prep.items():
            for prep in l_prep:
                if prep.called is False:
                    return (argument, 'PREP')
        
        for argument, obj in self.registered.items():
            if obj.called is False:
                return (argument, 'EXEC')
        
        return ('UNKNOWN', 'UNKNOWN')
    
    @property
    def validate(self) -> bool:
        # Check all preps
        for _, l_prep in self.prep.items():
            for prep in l_prep:
                if prep.called is False:
                    return False
        
        # check executions
        # If both lengths are same, all are executed.
        return len(self.registered) == len(self.executed)
    
    def if_exec(self, argument: str) -> bool:
        return argument in self.executed
    
    def result_of(self, argument: str, default: Union[Any, None] = None) -> Any:
        if argument in self.executed:
            for name, obj in self.executed.items():
                if name == argument:
                    return obj.results
            return default
        else:
            return default