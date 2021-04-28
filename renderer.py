import numpy as np
import math
import os
from PIL import Image, ImageChops
from scene.ray import Ray
from utils import progress, split_range, reflect, refract, importance_sample_hemisphere
from materials.transmissive_material import TransmissiveMaterial
from scene.point_light import PointLight
from multiprocessing import Process
import scene


class Renderer:
    def __init__(self, scene, max_depth, max_rays=100, k_a=0.1):
        self.scene = scene
        self.max_depth = max_depth
        self.bias = 1e-4
        self.max_rays = max_rays
        self.k_a = k_a

    def render_part(self, cam, top_left, increment, start, end, im, o_im, path, name):
        for i in range(start, end):
            for j in range(cam.height):
                point = top_left + (i * increment * cam.u) + (j * increment * cam.v)
                if path:
                    color = self.path_trace(Ray(cam.cam_from, point))
                else:
                    color = self.ray_trace(Ray(cam.cam_from, point))
                im.putpixel((i, j), tuple((color * 255).astype(np.int64)))

                if o_im is not None:
                    o_color = self.ambient_occlusion(Ray(cam.cam_from, point))
                    o_im.putpixel((i, j), tuple((o_color * 255).astype(np.int64)))
                progress((i - start) * cam.height + j, (end - start) * cam.height)
        im.save(name)
        if o_im is not None:
            o_im.save('o' + name)

    def render(self, process_count, occlusion=False, path=False):
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
            o_im = Image.new('RGB', (cam.width, cam.height)) if occlusion else None
            process = Process(target=self.render_part,
                              args=(cam, top_left, increment, start, end, im, o_im, path, 'tmp' + str(i) + '.png'))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()

        im = Image.new('RGB', (cam.width, cam.height))
        for i in range(process_count):
            im_tmp = Image.open('tmp' + str(i) + '.png')
            im = ImageChops.add(im, im_tmp)
            os.remove('tmp' + str(i) + '.png')

        o_im, f_im = None, None
        if occlusion:
            o_im = Image.new('RGB', (cam.width, cam.height))
            for i in range(process_count):
                o_im_tmp = Image.open('otmp' + str(i) + '.png')
                o_im = ImageChops.add(o_im, o_im_tmp)
                os.remove('otmp' + str(i) + '.png')
            f_im = ImageChops.add(im, Image.fromarray(np.uint8(self.k_a * np.array(o_im))))
        return im, o_im, f_im

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

    def is_occluded(self, ray, dist):
        for obj in self.scene.objects:
            if type(obj.material) is TransmissiveMaterial:
                continue
            hit_dist = obj.get_intersection(ray)
            if hit_dist is not None and hit_dist < dist:
                return True
        return False

    def ambient_occlusion(self, ray):
        ambient_color = np.array([0.5, 0.5, 0.5])
        max_rays = 50
        max_dist = 20
        occlusion = 0
        dist, obj = self.find_nearest_hit(ray)
        if dist is None:
            return np.array([0, 0, 0], dtype=np.float32)
        point = ray.origin + ray.dir * dist
        normal = obj.get_normal(point)
        for i in range(max_rays):
            direction, prob = importance_sample_hemisphere(normal)
            new_ray = Ray(point + normal * self.bias, None, direction)
            vis = 1
            if self.is_occluded(new_ray, max_dist):
                vis = 0
            occlusion += vis * np.dot(new_ray.dir, normal) / (math.pi * prob)
        return (occlusion / max_rays) * ambient_color
    
    def ray_trace(self, ray, depth=0):
        # Find nearest intersection for ray, compute reflected ray and call recursively
        # with depth += 1 until depth == max_depth or no intersection is found.
        color = np.array([0, 0, 0], dtype=np.float32)
        dist, obj = self.find_nearest_hit(ray)
        if dist is None:
            return color
        point = ray.origin + ray.dir * dist
        normal = obj.get_normal(point)
        if np.dot(-ray.dir, normal) < 0:
            normal = -normal

        lights = []
        for light in self.scene.lights:
            dist = math.inf
            if type(light) == scene.point_light.PointLight:
                dist = np.linalg.norm(point - light.pos)
            if not self.is_blocked(point + normal * self.bias, light, dist):
                lights.append(light)

        color += obj.material.get_color(point, normal, ray, lights)

        if depth < self.max_depth:
            if type(obj.material) is not TransmissiveMaterial:
                color += self.ray_trace(Ray(point + normal * self.bias, None,
                                            reflect(ray.dir, normal)), depth + 1) * obj.material.ref
            else:
                kr = obj.material.fresnel(ray.dir, normal)
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
                if outside:
                    reflection_orig = point + bias
                else:
                    reflection_orig = point - bias
                reflection_col = self.ray_trace(Ray(reflection_orig, None, reflection_dir), depth + 1)
                color += (reflection_col * kr + refraction_col * (1 - kr))
        return color

    def path_trace(self, ray):
        color = np.array([0, 0, 0], dtype=np.float32)
        dist, obj = self.find_nearest_hit(ray)
        if dist is None:
            return color

        def trace_random_path(ray, depth=0):
            color = np.array([0, 0, 0], dtype=np.float32)
            dist, obj = self.find_nearest_hit(ray)
            if dist is None:
                return color
            point = ray.origin + ray.dir * dist
            normal = obj.get_normal(point)
            if np.dot(-ray.dir, normal) < 0:
                normal = -normal

            lights = []
            for light in self.scene.lights:
                dist = math.inf
                if type(light) == scene.point_light.PointLight:
                    dist = np.linalg.norm(point - light.pos)
                if not self.is_blocked(point + normal * self.bias, light, dist):
                    lights.append(light)

            for light in lights:
                w_i = Ray(point, None, -light.get_dir(point))
                color += light.col * light.get_intensity(point) * \
                         obj.material.brdf(normal, ray, w_i) * np.dot(normal, w_i.dir)

            if depth < self.max_depth:
                direction, prob = importance_sample_hemisphere(normal)
                new_ray = Ray(point + normal * self.bias, None, direction)
                color += trace_random_path(new_ray, depth + 1) * obj.material.brdf(normal, ray, new_ray) * \
                         np.dot(normal, new_ray.dir) / prob
            return color

        for i in range(self.max_rays):
            color += trace_random_path(ray)
        return color / self.max_rays
