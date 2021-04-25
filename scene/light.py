from abc import abstractmethod
import numpy as np


class Light:
    def __init__(self, col, intensity):
        self.col = np.array(col)
        self.intensity = intensity

    @abstractmethod
    def get_intensity(self, point):
        pass

    @abstractmethod
    def get_dir(self, point):
        pass
