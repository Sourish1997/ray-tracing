import math
from .object import Object
import numpy as np


class Plane(Object):
    def __init__(self, point0, normal, **kwargs):
        super().__init__(**kwargs)
        self.point0 = point0
        self.normal = normal

    def get_intersection(self, ray):
        # Returns distance from ray origin
        n_dot_l = np.dot(self.get_normal(0), ray.dir)

        if n_dot_l > 1e-6:
            t = np.dot(np.subtract(self.point0, ray.origin), self.get_normal(0)) / n_dot_l
            return t if t >= 0 else None

        return None

    def get_normal(self, point):
        # Return normalized normal
        return self.normal / np.linalg.norm(self.normal)
