import numpy as np
from .object import Object


class Cuboid(Object):
    def __init__(self, center, vmin, vmax, material):
        super().__init__(material)
        self.center = np.array(center)
        self.vmin = self.center + np.array(vmin)
        self.vmax = self.center + np.array(vmax)

    def get_intersection(self, ray):
        # Returns distance from ray origin
        tnear = float('-inf')
        tfar = float('inf')
        for i in range(3):
            if ray.dir[i] == 0:
                if ray.origin[i] < self.vmin[i] or ray.origin[i] > self.vmax[i]:
                    return None
            else:
                t1 = (self.vmin[i] - ray.origin[i]) / ray.dir[i]
                t2 = (self.vmax[i] - ray.origin[i]) / ray.dir[i]
                if t1 > t2:
                    t1, t2 = t2, t1
                if t1 > tnear:
                    tnear = t1
                if t2 < tfar:
                    tfar = t2
                if tnear > tfar:
                    return None
                if tfar < 0:
                    return None
        return tnear

    def get_normal(self, point):
        # Returns normalized surface normal at point
        EPS = 1e-4
        x_norm = np.array([1, 0, 0])
        y_norm = np.array([0, 1, 0])
        z_norm = np.array([0, 0, 1])

        if np.abs(point[0] - self.vmin[0]) < EPS:
            return -x_norm
        elif np.abs(point[0] - self.vmax[0]) < EPS:
            return x_norm
        elif np.abs(point[1] - self.vmin[1]) < EPS:
            return -y_norm
        elif np.abs(point[1] - self.vmax[1]) < EPS:
            return y_norm
        elif np.abs(point[2] - self.vmin[2]) < EPS:
            return -z_norm
        elif np.abs(point[2] - self.vmax[2]) < EPS:
            return z_norm
