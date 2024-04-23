from pge.core import Sprite

import typing

class SpriteList(list):
    '''
    Helper container for sorting sprite objects
    '''

    def sort_list(self) -> None:
        '''
        Sort the list based on the sprite's `index` value
        '''

        self.sort(key = lambda sprite: sprite.index)

    def append(self, __object: Sprite) -> None:
        if not isinstance(__object, Sprite):
            print(f'[SpriteList] Append Failed: {__object} not {Sprite.__name__}')
            return

        super().append(__object)
        self.sort_list()

    def extend(self, __iterable: typing.Sequence[Sprite]) -> None:
        for __object in __iterable:
            if not isinstance(__object, Sprite):
                print(f'[SpriteList] Extend Failed: {__object} not {Sprite.__name__}')
                return

        super().extend(__iterable)
        self.sort_list()

    def remove(self, __object: Sprite) -> None:
        if not isinstance(__object, Sprite):
            print(f'[SpriteList] Remove Failed: {__object} not {Sprite.__name__}')
            return

        super().remove(__object)
        self.sort_list()
