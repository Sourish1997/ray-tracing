import numpy as np
import math


class Camera:
    def __init__(self, **kwargs):
        self.cam_from = np.array(kwargs['from'])
        self.cam_to = np.array(kwargs['to'])
        self.u = np.array(kwargs['u']) / np.linalg.norm(np.array(kwargs['u']))
        self.v = np.array(kwargs['v']) / np.linalg.norm(np.array(kwargs['v']))
        self.width, self.height = kwargs['resolution']
        self.fov = math.pi / kwargs['fov']
