import numpy as np
import math
import os
from PIL import Image, ImageChops
from scene.ray import Ray
from utils import progress, split_range
from multiprocessing import Process
import scene


class Renderer:
    def __init__(self, scene, max_depth):
        self.scene = scene
        self.max_depth = max_depth

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
            hit_dist = obj.get_intersection(ray)
            if hit_dist is not None and hit_dist < dist:
                return True
        return False

    """
    TODO: Ambient Occlusion

    Useful References:
    ------------------
    https://www.gamedev.net/tutorials/programming/graphics/a-simple-and-practical-approach-to-ssao-r2753/

    https://www.davepagurek.com/blog/realtime-shadows/

    Variables:
    ---------
    tcoord: normal texture
    uv: value of uv
    p: position of uv
    cnorm: normal of uv
    g_scale: scales distance between occluders and occludee.
    g_intensity: the ao intensity. Once you tweak the values a bit and see how the AO reacts to them, it becomes very intuitive to achieve the effect you want.
    g_bias: controls the width of the occlusion cone considered by the occludee.

    """
    def doAmbientOcclusion(self, tcoord, uv, p, cnorm):
        diff = getPosition(tcoord + uv) - p
        v = normalize(diff)
        d = len(diff)*g_scale
        return max(0.0,np.dot(cnorm,v)-g_bias)*(1.0/(1.0+d))*g_intensity
    
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
            if not self.is_blocked(point + normal * 1e-4, light, dist):
                lights.append(light)
        color += obj.material.get_color(point, normal, self.scene.cam, lights)
        if depth < self.max_depth:
            color += self.ray_trace(Ray(point + normal * 1e-4, None, ray.dir - 2 * np.dot(ray.dir, normal) * normal),
                                    depth + 1) * obj.material.ref
        return color
