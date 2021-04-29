import numpy as np
import random
from math import sin, cos, acos, asin, sqrt, pi


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    print('\r[%s] %s%s ...%s' % (bar, percents, '%', suffix), end='')


def split_range(count, parts):
    d, r = divmod(count, parts)
    return [
        (i * d + min(i, r), (i + 1) * d + min(i + 1, r)) for i in range(parts)
    ]


def clamp(low, high, val):
    return min(max(low, val), high)


def reflect(i, n):
    return i - 2 * np.dot(n, i) * n


def refract(i, n, ior):
    cos_i = clamp(-1, 1, np.dot(n, i))
    eta_i = 1
    eta_t = ior
    n = n
    if cos_i < 0:
        cos_i = -cos_i
    else:
        eta_i, eta_t = eta_t, eta_i
        n = -n
    eta = eta_i / eta_t
    k = 1 - eta * eta * (1 - cos_i * cos_i)
    if k < 0:
        return 0
    else:
        return eta * i + (eta * cos_i - np.sqrt(k)) * n


def importance_sample_hemisphere(n):
    eta_i = random.uniform(0, 1)
    eta_j = random.uniform(0, 1)
    phi = 2 * pi * eta_i
    theta = asin(sqrt(eta_j))

    l_u = sin(theta) * cos(phi)
    l_v = cos(theta)
    l_w = sin(theta) * sin(phi)

    u = np.random.randn(3)  # take a random vector
    u -= u.dot(n) * n  # make it orthogonal to k
    u /= np.linalg.norm(u)
    w = np.cross(n, u)
    w /= np.linalg.norm(w)

    return u * l_u + n * l_v + w * l_w, cos(theta) * sin(theta) / pi
