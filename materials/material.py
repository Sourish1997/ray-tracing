from abc import abstractmethod
import numpy as np


class Material:
    def __init__(self, col, amb, dif, spec, ref, n):
        self.col = np.array(col)
        self.amb = amb
        self.dif = dif
        self.spec = spec
        self.ref = ref
        self.n = n

    @abstractmethod
    def get_color(self, point, normal, camera, light):
        pass
