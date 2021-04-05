import numpy as np


class Ray:
    def __init__(self, origin, dest, dir=None):
        self.origin = origin
        if dest is None:
            self.dir = dir / np.linalg.norm(dir)
        else:
            self.dir = (dest - origin) / np.linalg.norm(dest - origin)
