from pge.types import Singleton

import pygame
import typing

FuncInfo = typing.NewType('FuncInfo', tuple[typing.Sequence[any], typing.Union[None, int, typing.Sequence[int]]])

@Singleton
class Input:
    def __init__(self):
        self.pressed: pygame.key.ScancodeWrapper = None

        self._keydown_funcs: dict[callable, FuncInfo] = {}
        self._keyup_funcs: dict[callable, FuncInfo] = {}

        self._itering = False
        self._del_funcs: dict[int, list[callable]] = {
            pygame.KEYDOWN: [],
            pygame.KEYUP: []
        }

    def _iter_funcs(self, event: pygame.Event, funcs: dict[callable, FuncInfo]) -> None:
        self._itering = True

        key: int = event.key
        for func, info in funcs.items():
            if isinstance(info[1], typing.Sequence):
                if key in info[1]:
                    try:
                        func(*info[0], event)
                    except TypeError:
                        func(*info[0])    
        
            elif not info[1] or info[1] == key:
                try:
                    func(*info[0], event)
                except TypeError:
                    func(*info[0])    

        self._itering = False

        for key_type, funcs in self._del_funcs.items():
            for func in funcs:
                if key_type == pygame.KEYDOWN:
                    del self._keydown_funcs[func]
                elif key_type == pygame.KEYUP:
                    del self._keyup_funcs[func]    

        self._del_funcs[pygame.KEYDOWN].clear()   
        self._del_funcs[pygame.KEYUP].clear()

    def _run(self, events: list[pygame.Event]) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return True
            
            if event.type == pygame.KEYDOWN:
                self._iter_funcs(event, self._keydown_funcs)

            if event.type == pygame.KEYUP:
                self._iter_funcs(event, self._keyup_funcs)

        self.pressed = pygame.key.get_pressed()

        return False

    def connect(self, keys: typing.Union[None, int, typing.Sequence[int]],
                key_type: int, func: callable, *args: typing.Sequence[any]) -> None:
    
        assert key_type == pygame.KEYDOWN or key_type == pygame.KEYUP

        if key_type == pygame.KEYDOWN:
            self._keydown_funcs[func] = (args, keys)
        elif key_type == pygame.KEYUP:
            self._keyup_funcs[func] = (args, keys)

    def disconnect(self, func: callable, key_type: int) -> None:
        assert key_type == pygame.KEYDOWN or key_type == pygame.KEYUP
      
        if key_type == pygame.KEYDOWN:
            if not self._itering:
                del self._keydown_funcs[func]
            else:
                self._del_funcs[pygame.KEYDOWN].append(func)

        elif key_type == pygame.KEYUP:
            if not self._itering:
                del self._keyup_funcs[func]
            else:
                self._del_funcs[pygame.KEYUP].append(func)
