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
                color = self.ray_trace(Ray(cam.cam_from, point))
                im.putpixel((i, j), tuple((color * 255).astype(np.int64)))
        return im

    def find_nearest_hit(self, ray):
        dist_min = None
        obj_nearest = None
        for obj in self.scene.objects:
            dist = obj.get_intersection(ray)
            if dist is not None and (obj_nearest is None or dist < dist_min):
                dist_min = dist
                obj_nearest = obj
        return dist_min, obj_nearest

    def ray_trace(self, ray, depth=0):
        # Find nearest intersection for ray, compute reflected ray and call recursively
        # with depth += 1 until depth == max_depth or no intersection is found.
        color = np.array([0, 0, 0], dtype=np.float32)
        dist, obj = self.find_nearest_hit(ray)
        if dist is None:
            return color
        point = ray.origin + ray.dir * dist
        normal = obj.get_normal(point)
        color += obj.material.get_color(point, normal, self.scene.cam, self.scene.light)
        if depth < self.max_depth:
            color += self.ray_trace(Ray(point + normal * 1e-4, None, ray.dir + 2 * np.dot(ray.dir, normal) * normal),
                                    depth + 1) * obj.material.ref
        return color
