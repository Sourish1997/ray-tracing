from .material import Material
import numpy as np
import math


class BaseMaterial(Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_color(self, point, normal, camera, light):
        # --AMBIENT LIGHT--
        # ambient = Ka * ambient color, assuming Ka = self.amb and ambient color = self.col (material color)
        #
        # # --DIFFUSE LIGHT--
        # # Find dot product between L (light ray direction) and N (surface normal)
        # L = [light.pos[0], light.pos[1], light.pos[2]]
        # N = [normal[0], normal[1], normal[2]]
        # NdotL = numpy.dot(N, L)
        #
        # # diffuse = Kd * N.L * directional color, assuming Kd = self.diff
        # diffR = self.dif[0]*light.col[0]*NdotL
        # diffG = self.dif[1]*light.col[1]*NdotL
        # diffB = self.dif[2]*light.col[2]*NdotL

        # n_dot_l = np.dot(light.light_cam, normal)
        #
        # # Normalize the dot product
        # if n_dot_l < 0:
        #     n_dot_l = -n_dot_l
        #
        # if n_dot_l > 1:
        #     n_dot_l = 1
        #
        # d_r = light.col[0] * 0.4 * self.col[0] * self.dif * n_dot_l
        # d_g = light.col[1] * 0.4 * self.col[1] * self.dif * n_dot_l
        # d_b = light.col[2] * 0.4 * self.col[2] * self.dif * n_dot_l
        #
        # # --SPECULAR LIGHT--
        # # Calculate E (eye ray direction), and find dot product between N and E
        # oldE = [0, 0, -1]
        # EMag = math.sqrt((oldE[0]*oldE[0])+(oldE[1]*oldE[1])+(oldE[2]*oldE[2]))
        # E = [oldE[0]/EMag,
        #     oldE[1]/EMag,
        #     oldE[2]/EMag]
        # NdotE = numpy.dot(N, E)
        #
        # # If NdotL and NdotE are both positive, compute lighting model
        # if NdotL > 0.00 and NdotE > 0.00:
        #     # Normalize R
        #     oldR = [2*NdotL*(N[0]-L[0]), 2*NdotL*(N[1]-L[1]), 2*NdotL*(N[2]-L[2])]
        #     RMag = math.sqrt((oldR[0]*oldR[0])+(oldR[1]*oldR[1])+(oldR[2]*oldR[2]))
        #     R = [oldR[0]/RMag, oldR[1]/RMag, oldR[2]/RMag]
        #
        #     # Find dot product between R and E
        #     RdotE = numpy.dot(R, E)
        #
        # # If NdotL and NdotE are both negative, invert normal and compute lighting model
        # elif NdotL < 0.00 and NdotE < 0.00:
        #     # Invert N and normalize
        #     NMag = math.sqrt((N[0]*N[0])+(N[1]*N[1])+(N[2]*N[2]))
        #     Ninvert = [N[0]/NMag, N[1]/NMag, N[2]/NMag]
        #
        #     # Find dot product between N inverse and L
        #     NinvertdotL = numpy.dot(Ninvert, L)
        #
        #     # Normalize R
        #     oldR = [2*NinvertdotL*(Ninvert[0]-L[0]), 2*NinvertdotL*(Ninvert[1]-L[1]), 2*NinvertdotL*(Ninvert[2]-L[2])]
        #     RMag = math.sqrt((oldR[0]*oldR[0])+(oldR[1]*oldR[1])+(oldR[2]*oldR[2]))
        #     R = [oldR[0]/RMag, oldR[1]/RMag, oldR[2]/RMag]
        #
        #     # Find dot product between R and E
        #     RdotE = numpy.dot(R, E)
        #
        # # If NdotL and NdotE have different signs, set R to 0
        # else:
        #     R = [0, 0, 0]
        #     RdotE = numpy.dot(R, E)
        #
        # # specular = Ks * (R.E)^n * directional color, assuming Ks = self.spec, assuming n is not defined somewhere already
        # n = 2
        # specR = self.spec[0]*light.col[0]*pow(RdotE, n)
        # specG = self.spec[1]*light.col[1]*pow(RdotE, n)
        # specB = self.spec[2]*light.col[2]*pow(RdotE, n)
        #
        # # Combine all seperated light values together
        # red = int(max(0,min((ambR+diffR+specR) * 255,255)))
        # green = int(max(0,min((ambG+diffG+specG) * 255,255)))
        # blue = int(max(0,min((ambB+diffB+specB) * 255,255)))

        # c_r = self.amb * light.col[0] * self.col[0] * 0.05
        # c_g = self.amb * light.col[1] * self.col[1] * 0.05
        # c_b = self.amb * light.col[2] * self.col[2] * 0.05

        # c_r = self.spec * light.col[0] * self.col[0] * pow(max(0, np.dot(r, camera.cam_from - point)), self.n)
        # c_g = self.spec * light.col[1] * self.col[1] * pow(max(0, np.dot(r, camera.cam_from - point)), self.n)
        # c_b = self.spec * light.col[2] * self.col[2] * pow(max(0, np.dot(r, camera.cam_from - point)), self.n)

        # Lambertian shading for Diffuse:
        n_dot_l = np.dot(unitize(np.array(light.pos - point)), normal)

        c_r = self.dif * light.col[0] * self.col[0] * max(0, n_dot_l)
        c_g = self.dif * light.col[1] * self.col[1] * max(0, n_dot_l)
        c_b = self.dif * light.col[2] * self.col[2] * max(0, n_dot_l)

        r = -1 * np.array(light.pos) + 2 * n_dot_l * normal

        return np.array([c_r, c_g, c_b])
        # return [red, green, blue]
        # return self.col * 0.5


def unitize(cam_unit):
    """
    Function to unitize the matrix
    :param cam_unit: input matrix
    :return:

    """
    # Get the magnitude of the vector:

    size = math.sqrt(pow(cam_unit[0], 2) + pow(cam_unit[1], 2) + pow(cam_unit[2], 2))

    return [cam_unit[0]/size, cam_unit[1]/size, cam_unit[2]/size]
