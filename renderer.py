import numpy as np
import math
import os
from PIL import Image, ImageChops
from scene.ray import Ray
from utils import progress, split_range, reflect, refract, fresnel
from materials.transmissive import Transmissive
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
            if type(obj.material) is Transmissive:
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
            if type(obj.material) is not Transmissive:
                color += obj.material.get_color(point, normal, self.scene.cam, lights)
                # color += self.ray_trace(Ray(point + normal * self.bias, None, ray.dir - 2 * np.dot(ray.dir, normal) * normal), depth + 1) * obj.material.ref
                color += self.ray_trace(Ray(point + normal * self.bias, None, reflect(ray.dir, normal)), depth + 1) * obj.material.ref
            else:
                kr = fresnel(ray.dir, normal, obj.material.ior)
                color += obj.material.get_color(point, normal, self.scene.cam, lights, kr)
                outside = np.dot(ray.dir, normal) < 0
                bias = self.bias * normal
                refractionColor = np.zeros(3)
                if kr < 1:
                    if outside:
                        refractionOrig = point - bias
                    else:
                        refractionOrig = point + bias
                    refractionDir = refract(ray.dir, normal, obj.material.ior)
                    refractionColor = self.ray_trace(Ray(refractionOrig, None, refractionDir), depth + 1)
                reflectionDir = reflect(ray.dir, normal)
                reflectionColor = self.ray_trace(Ray(point + bias, None, reflectionDir), depth + 1)
                color += (reflectionColor * kr + refractionColor * (1 - kr))
        return color
