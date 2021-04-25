from .material import Material
import numpy as np
import math


class BaseMaterial(Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_color(self, point, normal, camera, lights):
        c_rgb = np.zeros(3)

        for i in range(len(lights)):
            # Lambertian shading for Diffuse:
            n_dot_l = np.dot(-lights[i].get_dir(point), normal)

            # Specular shading
            v = (camera.cam_from - point) / np.linalg.norm((camera.cam_from - point))
            h = (-lights[i].get_dir(point) + v) / np.linalg.norm(-lights[i].get_dir(point) + v)
            n_dot_h = np.dot(h, normal)

            c_rgb += (lights[i].col * lights[i].get_intensity(point)) * \
                     ((self.col * self.dif * max(0, n_dot_l) / math.pi) + (self.spec * pow(max(0, n_dot_h), self.n)))

        return c_rgb
