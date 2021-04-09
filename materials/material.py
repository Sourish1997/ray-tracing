from abc import abstractmethod


class Material:
    def __init__(self, col, amb, dif, spec, ref, n):
        self.col = col
        self.amb = amb
        self.dif = dif
        self.spec = spec
        self.ref = ref
        self.n = n

    @abstractmethod
    def get_color(self, point, normal, camera, light):
        pass
