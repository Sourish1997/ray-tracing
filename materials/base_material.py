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

            # specularity
            r = -1 * light[i].pos / np.linalg.norm(light[i].pos) + 2 * n_dot_l * normal
            h = (light[i].pos + np.array(camera.v2 - point)) / np.linalg.norm((light[i].pos + np.array(camera.v2 - point)))
            n_dot_h = np.dot(h, normal)

            c_rgb += light[i].col * self.col * (self.dif * max(0, n_dot_l) + (light[i].intensity * self.spec * pow(max(0, n_dot_h), self.n)))

        return c_rgb
