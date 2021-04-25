from .light import Light
import numpy as np
import math


class PointLight(Light):
    def __init__(self, **kwargs):
        super().__init__(kwargs['color'], kwargs['intensity'])
        self.pos = np.array(kwargs['pos'])

    def get_intensity(self, point):
        return (self.intensity * self.col) / (4 * math.pi * np.linalg.norm(point - self.pos))

    def get_dir(self, point):
        return (point - self.pos) / np.linalg.norm(point - self.pos)
