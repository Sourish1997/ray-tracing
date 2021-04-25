from .light import Light
import numpy as np


class DirLight(Light):
    def __init__(self, **kwargs):
        super().__init__(kwargs['color'], kwargs['intensity'])
        self.dir = (np.array(kwargs['to']) - np.array(kwargs['from'])) / \
                   np.linalg.norm(np.array(kwargs['to']) - np.array(kwargs['from']))

    def get_intensity(self, point):
        return self.intensity * self.col

    def get_dir(self, point):
        return self.dir
