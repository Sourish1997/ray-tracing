from .material import Material
import numpy as np
import math


class BaseMaterial(Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # NOTE: 'light' is a list of 'Light' objects from multiple light sources
    # TODO: need to add support for multiple lights as well
    def get_color(self, point, normal, camera, light):
        # Lambertian shading for Diffuse:
        n_dot_l = np.dot(light[0].pos / np.linalg.norm(light[0].pos), normal)

        # specularity
        r = -1 * light[0].pos / np.linalg.norm(light[0].pos) + 2 * n_dot_l * normal
        h = (light[0].pos + np.array(camera.v2 - point)) / np.linalg.norm((light[0].pos + np.array(camera.v2 - point)))
        n_dot_h = np.dot(h, normal)

        c_r, c_g, c_b = light[0].col * self.col * (self.dif * max(0, n_dot_l) + (light[0].intensity * self.spec * pow(max(0, n_dot_h), self.n)))

        return np.array([c_r, c_g, c_b])
