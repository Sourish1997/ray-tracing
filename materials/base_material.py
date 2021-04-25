from .material import Material
import numpy as np
import math


class BaseMaterial(Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # NOTE: 'light' is a list of 'Light' objects from multiple light sources
    # TODO: need to add support for multiple lights as well
    def get_color(self, point, normal, camera, light):
        c_rgb = np.zeros(3)

        for i in range(len(light)):
            # Lambertian shading for Diffuse:
            n_dot_l = np.dot(light[i].pos / np.linalg.norm(light[i].pos), normal)

            # Specular shading
            v = (camera.cam_from - point) / np.linalg.norm((camera.cam_from - point))
            h = (-light[i].get_dir(point) + v) / np.linalg.norm(-light[i].get_dir(point) + v)
            n_dot_h = np.dot(h, normal)

            c_rgb += (light[i].col * light[i].get_intensity(point)) * \
                     ((self.col * self.dif * max(0, n_dot_l) / math.pi) + (self.spec * pow(max(0, n_dot_h), self.n)))

        return c_rgb
