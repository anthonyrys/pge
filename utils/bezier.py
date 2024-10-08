from pge.types import Singleton

import dataclasses
import math
import typing

BezierInfo = typing.NewType('BezierInfo', typing.Sequence[typing.Union[tuple[int, int], int]])

@Singleton
class Bezier:
    class Presets:
        @property
        def SINE() -> BezierInfo:
            return [[0, 0], [0, 1], [1, 1], [1, 0], 0]

        @property
        def EASE_OUT() -> BezierInfo:
            return [[0, 0], [1, 0.09], [1, .95], [1, 0], 0]
        
        @property
        def EASE_IN() -> BezierInfo:
            return [[0, 0], [0, 0.09], [0, .95], [1, 0], 0]   

    @staticmethod
    def get_bezier_point(t: float, data: BezierInfo) -> float:
        p_0: tuple[float, float] = data[0]
        p_1: tuple[float, float] = data[1]
        p_2: tuple[float, float] = data[2]
        p_3: tuple[float, float] = data[3]

        p = [
            math.pow(1 - t, 3) * p_0[0]
            + 3 * t * math.pow(1 - t, 2) * p_1[0]
            + 3 * math.pow(t, 2) * (1 - t) * p_2[0]
            + math.pow(t, 3) * p_3[0],

            math.pow(1 - t, 3) * p_0[1]
            + 3 * t * math.pow(1 - t, 2) * p_1[1]
            + 3 * math.pow(t, 2) * (1 - t) * p_2[1]
            + math.pow(t, 3) * p_3[1]
        ]

        return p[data[4]]
