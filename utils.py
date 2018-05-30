import math
import org.babylonjs as api

"""module for utility math functions"""


def clamp(num: float, minimum: float, maximum: float) -> float:
    return min(max(num, minimum), maximum)


def lerp(alpha: float, a: float, b: float) -> float:
    alpha = clamp(alpha, 0, 1)
    return a * alpha + (b * (1 - alpha))


def smoothstep(x: float, lower: float, upper: float) -> float:
    x = clamp((x - lower) / (upper - lower), 0.0, 1.0)
    return x * x * (3 - 2 * x)


def ease_in(num: float, lower: float, upper: float) -> float:
    p = clamp(num, lower, upper) - lower / (upper - lower)
    alpha = math.pow(p, 2.0)
    return lerp(alpha, lower, upper)


def ease_out(num: float, lower: float, upper: float) -> float:
    p = clamp(num, lower, upper) - lower / (upper - lower)
    alpha = math.pow(p, 0.5)
    return lerp(alpha, lower, upper)

