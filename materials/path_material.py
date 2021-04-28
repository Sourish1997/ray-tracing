from abc import abstractmethod


class PathMaterial:
    def __init__(self, amb):
        self.amb = amb

    @abstractmethod
    def brdf(self, n, w_o, w_i):
        pass
