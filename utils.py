import numpy as np


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

