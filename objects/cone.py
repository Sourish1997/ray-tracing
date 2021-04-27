import math
from .object import Object
import numpy as np


class Cone(Object):
    def __init__(self, pa, p1, r1, material):
        super().__init__(material)
        self.base_p = np.array(pa)
        self.p1 = p1

        # self.base_p = base_p / np.linalg.norm(base_p)
        # self.axis_v = axis_v

        # self.axis_v_normalized = axis_v / np.linalg.norm(self.axis_v)
        # self.axis_v = axis_v / np.linalg.norm(axis_v)

        self.h = np.linalg.norm(np.subtract(pa, p1))
        self.axis_v = np.subtract(pa, p1) / self.h
        self.v = self.axis_v
        self.r1 = r1
        self.h_angle = np.arctan(r1 / self.h)

        print("height of the cone: {}".format(self.h))
        print("angle: {}".format(self.h_angle))
        print("pA: {}".format(self.base_p))
        print("p1: {}".format(self.p1))
        print("pV: {}".format(self.axis_v))

    def get_intersection(self, ray):
        dp = np.subtract(ray.origin, self.base_p)
        v = ray.dir

        p = ray.origin
        d = ray.dir

        v_dot_va = np.dot(v, self.axis_v)
        dp_dot_va = np.dot(dp, self.axis_v)

        v_sub_dot = v - v_dot_va * self.axis_v
        dp_sub_dot = dp - dp_dot_va * self.axis_v

        # One method:(PDF shared on Slack):

        a = pow(math.cos(self.h_angle * np.dot(v_sub_dot, v_sub_dot)), 2) - pow(math.sin(self.h_angle * (v_dot_va ** 2)), 2)
        b = 2 * pow(math.cos(self.h_angle * np.dot(v_sub_dot, dp_sub_dot)), 2) - 2 * pow(math.sin(self.h_angle * v_dot_va * dp_dot_va), 2)
        c = pow(math.cos(self.h_angle * np.dot(dp_sub_dot, dp_sub_dot)), 2) - pow(math.sin(self.h_angle * (dp_dot_va ** 2)), 2)


        # Alternative method: https://lousodrome.net/blog/light/2017/01/03/intersection-of-a-ray-and-a-cone/

        # a = pow(np.dot(self.v, d), 2) - pow(math.cos(self.h_angle), 2)
        # b = 2 * (np.dot(self.v, d) * np.dot((np.subtract(self.base_p, p)), self.v) - np.dot(d, np.subtract(self.base_p, p)) * pow(math.cos(self.h_angle), 2))
        # c = pow(np.dot((np.subtract(self.base_p, p)), self.v), 2) - np.dot(np.subtract(self.base_p, p),np.subtract(self.base_p, p)) * pow(math.cos(self.h_angle), 2)

        disc = b ** 2 - 4 * a * c

        if disc < 0:

            return None
        else:

            hit = min((-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a))

            if hit <= 0:

                return None

            return hit

    #
    def get_normal(self, point):

        # Generating normal: https://stackoverflow.com/questions/66343772/cone-normal-vector
        # d = np.subtract(self.base_p, point) * math.sqrt(1 + pow(math.tan(self.h_angle), 2))
        #
        # a = self.base_p + (self.axis_v * d)
        #
        # return np.subtract(point, a) / np.linalg.norm(np.subtract(point, a))

        # Alternative test method for generating normal:
        v = np.subtract(point, self.base_p) * (self.h / self.r1) / np.linalg.norm(np.subtract(point, self.base_p))

        return v / np.linalg.norm(v)
