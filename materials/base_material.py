from .material import Material


class BaseMaterial(Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_color(self, point, normal, light):
        # TODO: Implement Blinn/Phong here to get color
        pass
