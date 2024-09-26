from pge.utils import scale

import pygame
import typing

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: typing.Union[pygame.Surface, str], index: typing.Optional[int] = 0, 
                 position: typing.Optional[pygame.Vector2] = pygame.Vector2(0, 0),
                 image_scale: typing.Optional[float] = 1):

        pygame.sprite.Sprite.__init__(self)
        self.sprite_id: str = self.__class__.__name__

        if isinstance(image, pygame.Surface):
            self.image = image
        else:
            self.image: pygame.Surface = pygame.image.load(image)
            self.image = scale(self.image, image_scale)

        self.image.set_colorkey((0, 0, 0))

        self.original_image: typing.Final[pygame.Surface] = self.image.copy()

        self.index: int = index

        self.rect: pygame.FRect = self.image.get_frect(topleft=position)
        self.original_rect: typing.Final[pygame.FRect] = self.image.get_frect(topleft=position)

    @property
    def mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.image)
    
    @property
    def position(self) -> pygame.Vector2:
        return self.get_position()

    @property
    def dimensions(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.size)
    
    def get_position(self, point: str = 'topleft') -> pygame.Vector2:
        return pygame.Vector2(getattr(self.rect, point))

    def update(self) -> None:
        ...

    def render(self) -> None:
        ...
