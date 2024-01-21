from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: float
    y: float


def cross_product(p0: Point, p1: Point, p2: Point):
    """Cross product of vectors [p0->p1] and [p0->p2]."""
    return (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)


def compute_convex_hull(points: List[Point]):
    """Returns a convex hull of the given points.

    See https://e-maxx.ru/algo/convex_hull_graham for explanation.
    """
    if len(points) <= 3:
        return points

    points = sorted(points, key=lambda p: (p.x, p.y))

    bottom = []
    for p in points:
        while len(bottom) >= 2 and cross_product(bottom[-2], bottom[-1], p) <= 0:
            bottom.pop()
        bottom.append(p)

    up = []
    for p in reversed(points):
        while len(up) >= 2 and cross_product(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)

    bottom.extend(up[:-1])
    return bottom
