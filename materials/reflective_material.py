from .material import Material
import numpy as np


class ReflectiveMaterial(Material):
    def __init__(self, amb, ref):
        super().__init__(amb)
        self.ref = ref

    def get_color(self, point, normal, ray, lights):
        c_rgb = np.zeros(3)
        ambient = np.array([0.4, 0.4, 0.4])
        c_rgb += self.amb * ambient

        for i in range(len(lights)):
            a = lights[i].get_dir(point) / point
            if np.all(a == a[0]):
                c_rgb += (lights[i].col * lights[i].get_intensity(point) * self.ref)

        return c_rgb
