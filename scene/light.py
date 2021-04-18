import numpy as np


class Light:
    def __init__(self, **kwargs):
        self.col = np.array(kwargs["color"])
        self.pos = np.array(kwargs["pos"])
        self.intensity = kwargs["intensity"]
        self.light_id = kwargs["id"]
        self.light_type = kwargs["type"]
