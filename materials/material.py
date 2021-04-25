from abc import abstractmethod


class Material:
    def __init__(self, amb):
        self.amb = amb

    @abstractmethod
    def get_color(self, point, normal, camera, light):
        pass
