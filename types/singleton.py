import typing

T = typing.TypeVar('T')
class Singleton(typing.Generic[T]):
    def __init__(self, decorated: T):
        self._decorated: T = decorated
        self._instance: T = None

    def __call__(self, *args: typing.Sequence[any], **kwargs: dict[str, any]) -> T:
        if self._instance == None:
            self._instance = self._decorated(*args, **kwargs)
        
        return self._instance

    @property
    def instanced(self) -> bool:
        return self._instance is not None
