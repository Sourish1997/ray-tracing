from abc import abstractmethod


class Object:
    def __init__(self, center, material):
        self.center = center
        self.material = material

    @abstractmethod
    def get_intersection(self, ray):
        pass

    @abstractmethod
    def get_normal(self, point):
        pass

