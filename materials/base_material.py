from .material import Material
import numpy
import math


class BaseMaterial(Material):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # NOTE: 'light' is a list of 'Light' objects from multiple light sources
    # TODO: need to add support for multiple lights as well
    def get_color(self, point, normal, camera, light):
        # --AMBIENT LIGHT--
        # ambient = Ka * ambient color, assuming Ka = self.amb and ambient color = light.col
        # ambR = self.amb[0]*light[0].col[0]
        # ambG = self.amb[1]*light[0].col[1]
        # ambB = self.amb[2]*light[0].col[2]
        #
        # # --DIFFUSE LIGHT--
        # # Find dot product between L (light ray direction) and N (surface normal)
        # L = [light[0].pos[0], light[0].pos[1], light[0].pos[2]]
        # N = [normal[0], normal[1], normal[2]]
        # NdotL = numpy.dot(N, L)
        #
        # # diffuse = Kd * N.L * directional color, assuming Kd = self.diff
        # diffR = self.dif[0]*light[0].col[0]*NdotL
        # diffG = self.dif[1]*light[0].col[1]*NdotL
        # diffB = self.dif[2]*light[0].col[2]*NdotL
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
        # specR = self.spec[0]*light[0].col[0]*pow(RdotE, n)
        # specG = self.spec[1]*light[0].col[1]*pow(RdotE, n)
        # specB = self.spec[2]*light[0].col[2]*pow(RdotE, n)
        #
        # # Combine all seperated light values together
        # red = int(max(0,min((ambR+diffR+specR) * 255,255)))
        # green = int(max(0,min((ambG+diffG+specG) * 255,255)))
        # blue = int(max(0,min((ambB+diffB+specB) * 255,255)))

        # return [red, green, blue]
        return self.col * 0.5
