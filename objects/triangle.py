import math
from .object import Object
import numpy as np


class Triangle(Object):
    def __init__(self, v0, v1, v2, **kwargs):
        super().__init__(**kwargs)
        # Vertices of the triangle:
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        # Getting the normal, cross v1 - v0 and v2 - v0:
        self.a = np.subtract(v1, v0)
        self.b = np.subtract(v2, v0)
        self.normal = np.cross(self.a, self.b)

    def get_intersection(self, ray):
        # Implementation of the Moller Trumbore Ray Triangle Intersection algorithm:

        p_vec = np.cross(ray.dir, self.b)
        determinant = np.dot(self.a, p_vec)

        # Culling to discard backward facing triangles:
        if determinant < 1e-6:
            return None

        # Checking if the ray and the triangle are parallel:
        if abs(determinant) < 1e-6:
            return None

        t_vec = ray.origin - self.v0
        u = np.dot(t_vec, p_vec) / determinant

        if u < 0 or u > 1:
            return None

        q_vec = np.cross(t_vec, self.a)
        v = np.dot(ray.dir, q_vec) / determinant

        if v < 0 or (u + v) > 1:
            return None

        t = np.dot(self.b, q_vec) / determinant

        return t

    def get_normal(self, point):
        # Returns normalized normal:
        return self.normal / np.linalg.norm(self.normal)
