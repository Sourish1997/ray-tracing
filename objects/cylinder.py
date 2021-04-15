import math
from .object import Object
import numpy as np


class Cylinder(Object):
    # c = center, r = radius, h = height, v = axis direction vector
    # Cylinder equation: (q - c - v.(q - c)v)^2 - r^2 = 0
    def __init__(self, c, r, h, v, **kwargs):
        super().__init__(**kwargs)
        self.c = c
        self.r = r
        self.h = h
        self.v = v / np.linalg.norm(v)

    def get_intersection(self, ray):
        # Implement intersection math
        # Returns distance to hit from ray origin if hit is found else None
        p = ray.origin
        d = ray.dir

        a = (d - np.dot(self.v, d) * self.v)
        a = np.dot(a, a)
        b = 2 * np.dot((d - np.dot(d, self.v) * self.v), ((p - self.c) - np.dot(p - self.c, self.v) * self.v))
        c = ((p - self.c) - np.dot((p - self.c), self.v) * self.v)
        c = np.dot(c, c) - self.r**2

        disc = b ** 2 - 4 * a * c
        if disc < 0:
            return None
        else:
            hit = min((-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a))
            if hit <= 0:
                return None
            point = p + d * hit
            top = self.c + self.v * (self.h / 2)
            bottom = self.c - self.v * (self.h / 2)
            den = self.v[2] if self.v[2] != 0 else 1
            alpha = -self.v[0] / den
            beta = -self.v[1] / den
            lambda_1 = (self.v[0] * bottom[0] + self.v[1] * bottom[1] + self.v[2] * bottom[2]) / den
            lambda_2 = (self.v[0] * top[0] + self.v[1] * top[1] + self.v[2] * top[2]) / den

            if lambda_1 < point[2] - alpha * point[0] - beta * point[1] < lambda_2:
                return hit
            else:
                return None

    def get_normal(self, point):
        # Returns normalized surface normal at point
        n = (point - self.c) - np.dot(self.v, (point - self.c)) * self.v
        return n / np.linalg.norm(n)
