import typing

T = typing.TypeVar('T')
class Singleton(typing.Generic[T]):
    '''
    A helper class for singletons.
    
    This should be used as a decorator to the class that should be a 
    singleton. 

    The decorated class cannot be inherited from.
    '''

    def __init__(self, decorated: T) -> None:
        self._decorated: T = decorated
        self._instance: T = None

    def __call__(self, *args: typing.Sequence[any]) -> T:
        '''
        First call, it creates a new instance of the decorated class 
        and calls its `__init__` method with a sequence of `args`. 
        On all subsequent calls, the existing instance is returned.
        '''

        if (self._instance == None):
            self._instance = self._decorated(*args)
        
        return self._instance
