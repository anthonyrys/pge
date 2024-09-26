import inspect
import typing
import pygame
import math
import sys

T = typing.TypeVar('T')
def generate_import_dict(*excludes: typing.Sequence[T]) -> dict[str, T]:
    if not excludes:
        excludes = ()

    name: str = sys.modules[inspect.getmodule(inspect.stack()[1][0]).__name__]

    return {
        k: v for k, v in (c for c in inspect.getmembers(name, inspect.isclass) if c[0] not in excludes)
    }

def scale(image, sx: float, sy: typing.Optional[float] = None) -> pygame.Surface:
    if not sy: sy = sx
    return pygame.transform.scale(image, (image.get_width() * sx, image.get_height() * sy)).convert_alpha()

def clamp(v: float, mi: float, mx: float) -> float:
    return max(mi, min(v, mx))

def get_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    rx: float = abs(p1[0] - p2[0])
    ry: float = abs(p1[1] - p2[1])

    return math.sqrt(((rx **2) + (ry **2)))
