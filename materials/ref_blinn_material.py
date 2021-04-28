from .material import Material
import numpy as np
import math


class RefBlinnMaterial(Material):
    def __init__(self, col, amb, dif, spec, ref, n):
        super().__init__(amb)
        self.col = np.array(col)
        self.dif = dif
        self.spec = spec
        self.ref = ref
        self.n = n

    def get_color(self, point, normal, ray, lights):
        c_rgb = np.zeros(3)

        for i in range(len(lights)):
            # Lambertian shading for Diffuse:
            v = -ray.dir
            n_dot_l = np.dot(-lights[i].get_dir(point), normal)
            n_dot_v = np.dot(-ray.dir, normal)
            if n_dot_v < 0:
                return c_rgb

            # Specular shading
            h = (-lights[i].get_dir(point) + v) / np.linalg.norm(-lights[i].get_dir(point) + v)
            n_dot_h = np.dot(h, normal)

            c_rgb += (lights[i].col * lights[i].get_intensity(point)) * \
                     ((self.col * self.dif * max(0, n_dot_l) / math.pi) + (self.spec * pow(max(0, n_dot_h), self.n)))

        return c_rgb
