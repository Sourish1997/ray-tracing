from .path_material import PathMaterial
import numpy as np
import math


class PathBlinnMaterial(PathMaterial):
    def __init__(self, col, amb, dif, spec, n):
        super().__init__(amb)
        self.dif = np.array(dif) * np.array(col)
        self.spec = np.array(spec)
        self.n = n

    def brdf(self, n, w_o, w_i):
        if np.dot(n, w_i.dir) < 0:
            return np.zeros(3)
        h = (-w_o.dir + w_i.dir) / np.linalg.norm(-w_o.dir + w_i.dir)
        n_dot_h = np.dot(n, h)
        return (self.dif / math.pi) + (self.spec * (self.n + 8) / (8 * math.pi) * pow(math.cos(n_dot_h), self.n))
