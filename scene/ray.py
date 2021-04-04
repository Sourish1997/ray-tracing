import numpy as np


class Ray:
    def __init__(self, origin, dest):
        self.origin = origin
        self.dir = dest / np.linalg.norm(dest)
