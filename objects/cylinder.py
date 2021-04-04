import numpy as np
from .object import Object


class Cylinder(Object):
    def __init__(self, radius, height, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height

    def get_intersection(self, ray):
        # TODO: Implement intersection math, returns distance from ray origin
        pass

    def get_normal(self, point):
        # TODO: Returns normalized surface normal at point
        pass
