from pge.core import Sprite

import typing

class SpriteList(list):
    '''
    A generic helper container for storing sprite objects.
    '''

    def _sort_list(self) -> None:
        '''
        Sort the list based on the sprite's `index` value.
        '''

        self.sort(key = lambda sprite: sprite.index)

    def _get_type_error_message(self, __object: any) -> str:
        '''
        Returns a `TypeError` specific message.
        '''

        return f'{__object} ({__object.__class__.__name__}) not {Sprite.__name__}'
        
    def update_all(self) -> None:        
        '''
        For all sprites in the list, call its `update` function.
        '''

        for __object in self:
            __object.update()

    def render_all(self) -> None:
        '''
        For all sprites in the list, call its `render` function.
        '''
                
        for __object in self:
            __object.render()


    def __init__(self, __iterable: typing.Optional[typing.Sequence[Sprite]] = []) -> None:
        for __object in __iterable:
            if not isinstance(__object, Sprite):
                raise TypeError(f'[SpriteList] __init__ Failed: {self._get_type_error_message(__object)}')

        super().__init__(__iterable)
        
    def __setitem__(self, index: int, __object: Sprite) -> None:
        if not isinstance(__object, Sprite):
            raise TypeError(f'[SpriteList] __setitem__ Failed: {self._get_type_error_message(__object)}')

        super().__setitem__(index, __object)
        self._sort_list()


    def append(self, __object: Sprite) -> None:
        if not isinstance(__object, Sprite):
            raise TypeError(f'[SpriteList] append Failed: {self._get_type_error_message(__object)}')

        super().append(__object)
        self._sort_list()

    def extend(self, __iterable: typing.Sequence[Sprite]) -> None:
        for __object in __iterable:
            if not isinstance(__object, Sprite):
                raise TypeError(f'[SpriteList] extend Failed: {self._get_type_error_message(__object)}')

        super().extend(__iterable)
        self._sort_list()

    def insert(self, index: int, __object: Sprite, ) -> None:
        if not isinstance(__object, Sprite):
            raise TypeError(f'[SpriteList] insert Failed: {self._get_type_error_message(__object)}')

        super().insert(index, __object)
        self._sort_list()
