import math
from .object import Object
import numpy as np


class Cone(Object):
    def __init__(self, pa, p1, r1, material):
        super().__init__(material)
        self.p1 = np.array(p1)
        self.center = self.p1
        self.pa = np.array(pa)
        # right now va is hard coded for upright cone only, TODO refactor for any va 
        self.va = (np.array([0, 1, 0]) + self.pa - self.p1) / np.linalg.norm(np.array([0, 1, 0]) + self.pa - self.p1)
        self.r1 = r1
        self.h = np.linalg.norm(np.abs(np.subtract(self.pa, p1)))
        self.alpha = np.arctan(r1 / self.h)

        # self.pa = self.p1 + self.r1 * (self.p2 - self.p1) / (self.r1 - self.r2)
        # self.va = (self.p2 - self.p1) / np.linalg.norm(self.p2 - self.p1)
        # self.alpha = (self.r1 - self.r2) / np.linalg.norm(self.p2 - self.p1)

        print("height of the cone: {}".format(self.h))
        print("angle: {}".format(self.alpha))
        print("pA: {}".format(self.pa))
        print("p1: {}".format(self.center))
        # print("p2: {}".format(self.p2))
        print("pV: {}".format(self.va))

    def get_intersection(self, ray):
        p = ray.origin
        v = ray.dir
        p_delta = p - self.pa

        v_dot_va = np.dot(v, self.va)
        dp_dot_va = np.dot(p_delta, self.va)
        v_sub_dot = v - v_dot_va * self.va
        dp_sub_dot = p_delta - dp_dot_va * self.va
        cos_sq = math.cos(self.alpha) ** 2
        sin_sq = math.sin(self.alpha) ** 2

        a = cos_sq * np.dot(v_sub_dot, v_sub_dot) - sin_sq * (v_dot_va ** 2)
        b = 2 * cos_sq * np.dot(v_sub_dot, dp_sub_dot) - 2 * sin_sq * v_dot_va * dp_dot_va
        c = cos_sq * np.dot(dp_sub_dot, dp_sub_dot) - sin_sq * (dp_dot_va ** 2)
        disc = b ** 2 - 4 * a * c

        if disc < 0:
            return None
        else:
            hit = min((-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a))
            if hit <= 0:
                return None

            cp = p + hit * ray.dir - self.pa
            hit_h = np.dot(cp, self.va)
            if hit_h < 0 or hit_h > self.h:
                return None

        return hit

    def get_normal(self, point):

        # Generating normal: https://stackoverflow.com/questions/66343772/cone-normal-vector
        # d = np.subtract(self.base_p, point) * math.sqrt(1 + pow(math.tan(self.h_angle), 2))
        #
        # a = self.base_p + (self.axis_v * d)
        #
        # return np.subtract(point, a) / np.linalg.norm(np.subtract(point, a))

        # Alternative test method for generating normal:
        v = np.subtract(point, self.center) * (self.h / self.r1) / np.linalg.norm(np.subtract(point, self.center))

        return v / np.linalg.norm(v)