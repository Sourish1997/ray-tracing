from abc import abstractmethod


class Material:
    def __init__(self, col, amb, dif, spec, ref):
        self.col = col
        self.amb = amb
        self.dif = dif
        self.spec = spec
        self.ref = ref

    @abstractmethod
    def get_color(self, point, normal, light):
        pass
