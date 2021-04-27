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

def reflect(I, N):
    return I - 2 * np.dot(N, I) * N

def refract(I, N, ior):
    cosi = clamp(-1, 1, np.dot(N, I))
    etai = 1
    etat = ior
    n = N
    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        n = -n
    eta = etai / etat
    k = 1 - eta * eta * (1 - cosi * cosi)
    if k < 0:
        return 0
    else:
        return eta * I + (eta * cosi - np.sqrt(k)) * n

def fresnel(I, N, ior):
    cosi = clamp(-1, 1, np.dot(I, N))
    etai = 1
    etat = ior
    if cosi > 0:
        etai, etat = etat, etai
    sint = etai / etat * np.sqrt(max(0., 1 - cosi * cosi))
    if sint >= 1:
        kr = 1
    else:
        cost = np.sqrt(max(0., 1 - sint * sint))
        cosi = np.abs(cosi)
        Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
        Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
        kr = (Rs * Rs + Rp * Rp) / 2
    return kr
