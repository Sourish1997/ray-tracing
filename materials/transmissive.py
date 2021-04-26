from .material import Material
from scene.point_light import PointLight
from scene.dir_light import DirLight
import numpy as np
import math


class Transmissive(Material):
    def __init__(self, col, amb, dif, spec, ref, n, ior, **kwargs):
        super().__init__(amb)
        self.col = np.array(col)
        self.dif = dif
        self.spec = spec
        self.ref = ref
        self.n = n  # specular power
        self.ior = ior

    def get_color(self, point, normal, camera, lights, kr):
        c_rgb = np.zeros(3)

        for i in range(len(lights)):
            a = lights[i].get_dir(point) / point
            if np.all(a == a[0]):
                c_rgb += (lights[i].col * lights[i].get_intensity(point) * kr)

        return c_rgb
