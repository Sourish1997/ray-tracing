import numpy as np
from .object import Object


class Sphere(Object):
    def __init__(self, center, radius, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.radius = radius

    def get_intersection(self, ray):
        # Returns distance from ray origin

        # vectorized calculation
        b = 2 * np.sum(ray.dir * (ray.origin - self.center))
        c = np.square(ray.origin - self.center).sum() - np.square(self.radius)

        # a = 1 since ray dir is normalized
        a = 1
        d = np.square(b) - 4 * a * c  # discriminant
        if d < 0:
            return None

        t0 = (-b + np.sqrt(d)) / (2 * a)
        t1 = (-b - np.sqrt(d)) / (2 * a)

        return min(t0, t1)

    def get_normal(self, point):
        # Returns normalized surface normal at point
        return np.subtract(point, self.center) / np.linalg.norm(np.subtract(point, self.center))
