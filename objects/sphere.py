import numpy as np
from .object import Object


class Sphere(Object):
    def __init__(self, center, radius, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.radius = radius

    def get_intersection(self, ray):
        # TODO: Implement intersection math, returns distance from ray origin
        pass

    def get_normal(self, point):
        # TODO: Returns normalized surface normal at point
        pass
