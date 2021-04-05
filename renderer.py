import numpy as np
import math
from PIL import Image
from scene.ray import Ray


class Renderer:
    def __init__(self, scene, max_depth):
        self.scene = scene
        self.max_depth = max_depth

    def render(self):
        # Call ray trace for each pixel in image
        cam = self.scene.cam
        cam_to_screen = np.linalg.norm(cam.cam_to - cam.cam_from)
        screen_width = 2 * math.tan(cam.fov / 2) * cam_to_screen
        screen_height = screen_width * cam.height / cam.width
        increment = screen_width / cam.width
        top_left = cam.cam_to - ((screen_width / 2) * cam.u) - ((screen_height / 2) * cam.v)

        im = Image.new('RGB', (cam.width, cam.height))
        for i in range(cam.width):
            for j in range(cam.height):
                point = top_left + (i * increment * cam.u) + (j * increment * cam.v)
                color = self.ray_trace(Ray(cam.cam_from, point), self.max_depth)
                im.putpixel(tuple(i, j), tuple(color))

        return im

    def ray_trace(self, ray, depth=0):
        # TODO: Implement recursively. Find nearest intersection for ray, compute reflected ray and call recursively
        # with depth += 1 until depth == max_depth or no intersection is found.
        pass
