from .material import Material
from utils import clamp
import numpy as np


class TransmissiveMaterial(Material):
    def __init__(self, amb, ior):
        super().__init__(amb)
        self.ior = ior

    def fresnel(self, i, n):
        cos_i = clamp(-1, 1, np.dot(i, n))
        eta_i = 1
        eta_t = self.ior
        if cos_i > 0:
            eta_i, eta_t = eta_t, eta_i
        sin_t = eta_i / eta_t * np.sqrt(max(0., 1 - cos_i * cos_i))
        if sin_t >= 1:
            kr = 1
        else:
            cos_t = np.sqrt(max(0., 1 - sin_t * sin_t))
            cos_i = np.abs(cos_i)
            r_s = ((eta_t * cos_i) - (eta_i * cos_t)) / ((eta_t * cos_i) + (eta_i * cos_t))
            r_p = ((eta_i * cos_i) - (eta_t * cos_t)) / ((eta_i * cos_i) + (eta_t * cos_t))
            kr = (r_s * r_s + r_p * r_p) / 2
        return kr

    def get_color(self, point, normal, ray, lights):
        c_rgb = np.zeros(3)
        ambient = np.array([0.4, 0.4, 0.4])
        c_rgb += self.amb * ambient

        for i in range(len(lights)):
            a = lights[i].get_dir(point) / point
            if np.all(a == a[0]):
                c_rgb += (lights[i].col * lights[i].get_intensity(point) * self.fresnel(ray.dir, normal))

        return c_rgb
