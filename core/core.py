from pge import OPENGL, MOUSE

from pge.types import Singleton

from pge.utils import clamp

from pge.mgl import MGLRenderer

from pge.core import Input
from pge.core import Font
from pge.core import Sound

import pygame
import typing
import time

@Singleton
class Core:
    @Singleton
    class Services:
        def __init__(self):
            self.inputs: Input = Input()
            self.fonts: Font = Font()
            self.sounds: Sound = Sound()

    def __init__(self, title: str, screen_dimensions: tuple[int, int], frame_rate: int,
                 pygame_flags: typing.Optional[int] = 0, pge_flags: typing.Optional[int] = 0):

        if pge_flags & OPENGL:
            pygame_flags |= (pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption(title)
        pygame.mouse.set_visible(True if pge_flags & MOUSE else False)

        self.title: str = title
        
        self.screen_dimensions: tuple[int, int] = screen_dimensions
        self.frame_rate: int = frame_rate

        self.quit: bool = False

        self.screen: pygame.Surface = pygame.display.set_mode(screen_dimensions, pygame_flags)
        self.screen_color: tuple[int, int, int] = (0, 0, 0)

        self.opengl: bool = True if pge_flags & OPENGL else False
        self.mgl: MGLRenderer = None

        if self.opengl:
            self.mgl: MGLRenderer = MGLRenderer(screen_dimensions)

        self.clock: pygame.Clock = pygame.time.Clock()

        self.delta_time: float = time.time()
        self.last_time: float = time.time()
        self.delta_time_threshold: typing.Union[float, None] = None

        self.frame_count: float = 0

        self.events: list[pygame.Event] = None
        
        self.services: self.Services = self.Services()
        
    def __del__(self) -> None:
        pygame.mixer.quit()
        pygame.quit()

    def run(self, func: typing.Optional[typing.Callable] = None, *args: typing.Sequence[any]) -> None:
        while not self.quit:
            self.events = pygame.event.get()
            self.quit = self.services.inputs._run(self.events)
            
            self.delta_time = (time.time() - self.last_time) * self.frame_rate
            self.last_time = time.time()

            if self.delta_time_threshold:
                self.delta_time = clamp(self.delta_time, 0, self.delta_time_threshold)

            self.frame_count += 1 * self.delta_time
            
            if func:
                func(*args)

            if self.opengl:
                self.mgl.render()

            pygame.display.flip()

            self.clock.tick(self.frame_rate)
