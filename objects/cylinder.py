import math
from .object import Object
import numpy as np


class Cylinder(Object):
    # c = center, r = radius, h = height, v = axis direction vector
    # Cylinder equation: (q - c - v.(q - c)v)^2 - r^2 = 0
    def __init__(self, center, radius, h, v, material):
        super().__init__(material)
        self.c = np.array(center)
        self.r = radius
        self.h = h
        self.v = np.array(v) / np.linalg.norm(np.array(v))

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
            v1 = np.dot((point - bottom), self.v) * self.v
            v2 = np.dot((top - point), self.v) * self.v
            if np.linalg.norm(bottom + v1 + v2 - top) < 0.0001:
                return hit
            else:
                return None

    def get_normal(self, point):
        # Returns normalized surface normal at point
        n = (point - self.c) - np.dot(self.v, (point - self.c)) * self.v
        return n / np.linalg.norm(n)
