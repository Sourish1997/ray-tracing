import numpy as np
from .object import Object


class Sphere(Object):
    def __init__(self, center, radius, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.radius = radius

    def get_intersection(self, ray):
        # TODO: Implement intersection math, returns distance from ray origin
        # xd, yd, zd = ray.dir
        # x0, y0, z0 = ray.origin
        # xc, yc, zc = self.center

        # vectorized calculation
        b = 2 * np.sum(ray.dir * (ray.origin - self.center))
        c = np.square(ray.origin - self.center).sum() - np.square(self.radius)

        # a = 1 since ray dir is normalized
        a = 1
        d = np.sqrt(np.square(b) - 4 * a * c)   # discriminant
        if d < 0:
            return None

        t0 = (-b + d) / (2 * a)
        t1 = (-b - d) / (2 * a)

        return np.min(t0, t1)

    def get_normal(self, point):
        # TODO: Returns normalized surface normal at point
        return np.subtract(point, self.center) / np.linalg.norm(np.subtract(point, self.center))
