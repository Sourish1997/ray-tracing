from scene.camera import Camera
from scene.light import Light
from scene.scene import Scene
from renderer import Renderer
from objects.sphere import Sphere
from objects.cylinder import Cylinder
from materials.base_material import BaseMaterial
import numpy as np
import math


def main():
    # Create a scene object
    # TODO: Parse a JSON
    width = 512
    height = 512
    cam_from = np.array([2, -4, -8])
    cam_to = np.array([2, -3, -6])
    u = np.array([2, 0, 0])
    v = np.array([0, 2, -1])
    fov = math.pi / 3
    cam = Camera(cam_from, cam_to, u, v, fov, width, height)
    light = Light(np.array([1, 1, 1]), np.array([4, 4, -10]))
    prop = {'col': np.array([1, 0, 0]), 'amb': 0.4, 'dif': 0.6, 'spec': 0.5, 'ref': 0.8}
    prop_2 = {'col': np.array([0, 1, 0]), 'amb': 0.4, 'dif': 0.6, 'spec': 0.5, 'ref': 0.8}
    prop_3 = {'col': np.array([0, 0, 1]), 'amb': 0.4, 'dif': 0.6, 'spec': 0.5, 'ref': 0.8}
    mat = {'material': BaseMaterial(**prop)}
    mat_2 = {'material': BaseMaterial(**prop_2)}
    mat_3 = {'material': BaseMaterial(**prop_3)}
    cyl_1 = Cylinder(np.array([2, 0, 4]), 2, 12, np.array([0, 1, 0]), **mat_3)
    sph_1 = Sphere(np.array([0, 0, 0]), 2, **mat)
    sph_2 = Sphere(np.array([3, 0, 0]), 1, **mat_2)
    objects = [sph_1, sph_2, cyl_1]
    scene = Scene(cam, light, objects)
    # Create a renderer object with scene passed as param
    renderer = Renderer(scene, 3)
    # Call the renderer's render function
    im = renderer.render()
    im.save('img.png')


if __name__ == "__main__":
    main()
