import numpy as np
import math
import os
from PIL import Image, ImageChops
from scene.ray import Ray
from utils import progress, split_range, reflect, refract
from materials.transmissive_material import TransmissiveMaterial
from scene.point_light import PointLight
# import tqdm
from multiprocessing import Process
import scene


class Renderer:
    def __init__(self, scene, max_depth):
        self.scene = scene
        self.max_depth = max_depth
        self.bias = 1e-4

    def render_part(self, cam, top_left, increment, start, end, im, name):
        for i in range(start, end):
            for j in range(cam.height):
                point = top_left + (i * increment * cam.u) + (j * increment * cam.v)
                color = self.ray_trace(Ray(cam.cam_from, point))
                im.putpixel((i, j), tuple((color * 255).astype(np.int64)))
                progress((i - start) * cam.height + j, (end - start) * cam.height)
        im.save(name)

    def render(self, process_count):
        # Call ray trace for each pixel in image
        cam = self.scene.cam
        cam_to_screen = np.linalg.norm(cam.cam_to - cam.cam_from)
        screen_width = 2 * math.tan(cam.fov / 2) * cam_to_screen
        screen_height = screen_width * cam.height / cam.width
        increment = screen_width / cam.width
        top_left = cam.cam_to - ((screen_width / 2) * cam.u) - ((screen_height / 2) * cam.v)

        ranges = split_range(cam.width, process_count)
        processes = []
        for i, (start, end) in enumerate(ranges):
            im = Image.new('RGB', (cam.width, cam.height))
            process = Process(target=self.render_part,
                              args=(cam, top_left, increment, start, end, im, 'tmp_' + str(i) + '.png'))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()

        im = Image.new('RGB', (cam.width, cam.height))
        for i in range(process_count):
            im_tmp = Image.open('tmp_' + str(i) + '.png')
            im = ImageChops.add(im, im_tmp)
            os.remove('tmp_' + str(i) + '.png')
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

    def is_blocked(self, point, light, dist):
        ray = Ray(point, None, -light.get_dir(point))
        for obj in self.scene.objects:
            if type(obj.material) is TransmissiveMaterial:
                continue
            hit_dist = obj.get_intersection(ray)
            if hit_dist is not None and hit_dist < dist:
                return True
        return False
    
    def ray_trace(self, ray, depth=0):
        # Find nearest intersection for ray, compute reflected ray and call recursively
        # with depth += 1 until depth == max_depth or no intersection is found.
        color = np.array([0, 0, 0], dtype=np.float32)
        dist, obj = self.find_nearest_hit(ray)
        if dist is None:
            return color
        point = ray.origin + ray.dir * dist
        normal = obj.get_normal(point)

        lights = []
        for light in self.scene.lights:
            dist = math.inf
            if type(light) == scene.point_light.PointLight:
                dist = np.linalg.norm(point - light.pos)
            if not self.is_blocked(point + normal * self.bias, light, dist):
                lights.append(light)

        if depth < self.max_depth:
            if type(obj.material) is not TransmissiveMaterial:
                color += obj.material.get_color(point, normal, ray, lights)
                color += self.ray_trace(Ray(point + normal * self.bias, None,
                                            reflect(ray.dir, normal)), depth + 1) * obj.material.ref
            else:
                kr = obj.material.fresnel(ray.dir, normal)
                color += obj.material.get_color(point, normal, ray, lights)
                outside = np.dot(ray.dir, normal) < 0
                bias = self.bias * normal
                refraction_col = np.zeros(3)
                if kr < 1:
                    if outside:
                        refraction_orig = point - bias
                    else:
                        refraction_orig = point + bias
                    refraction_dir = refract(ray.dir, normal, obj.material.ior)
                    refraction_col = self.ray_trace(Ray(refraction_orig, None, refraction_dir), depth + 1)
                reflection_dir = reflect(ray.dir, normal)
                reflection_col = self.ray_trace(Ray(point + bias, None, reflection_dir), depth + 1)
                color += (reflection_col * kr + refraction_col * (1 - kr))
        return color
