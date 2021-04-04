class Renderer:
    def __init__(self, scene, max_depth):
        self.scene = scene
        self.max_depth = max_depth

    def render(self):
        # TODO: Call ray trace for each pixel in image
        pass

    def ray_trace(self, ray, scene, depth=0):
        # TODO: Implement recursively. Find nearest intersection for ray, compute reflected ray and call recursively
        # with depth += 1 until depth == max_depth or no intersection is found.
        pass
