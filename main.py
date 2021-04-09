from scene.camera import Camera
from scene.light import Light
from scene.scene import Scene
from renderer import Renderer
from objects.sphere import Sphere
from objects.cylinder import Cylinder
from materials.base_material import BaseMaterial
import numpy as np
import math
import json


def parse_scene_json(scene_json):
    """
    Param: scene_file - json file of scene description
    Returns: Scene obj to render
    """

    with open(scene_json, "r") as scene_des:
        scene = json.loads(scene_des.read())["scene"]

    # objs, lights, camera = scene["shapes"], scene["lights"], scene["camera"]
    # camera
    width, height = scene["camera"]["resolution"]
    cam_from = np.array(scene["camera"]["from"])
    cam_to = np.array(scene["camera"]["to"])
    u = np.array([2, 0, 0])
    v = np.array([0, 2, -1])
    fov = math.pi / 3
    cam = Camera(cam_from, cam_to, u, v, fov, width, height)

    # light (only support for point lights rn, requires refactoring of light.py)
    # TODO: need to add support for multiple lights as well
    light = Light(np.array(scene["lights"][0]["color"]), np.array(scene["lights"][0]["pos"]))

    objects = []
    for obj in scene["shapes"]:
        prop = {'col': np.array(obj["material"]["Cs"]), 'amb': obj["material"]["Ka"], 'dif': obj["material"]["Kd"], 'spec': obj["material"]["Ks"], 'ref': 0.8}
        mat = {'material': BaseMaterial(**prop)}
        geom_params = obj["geomParams"]
        if obj["geometry"] == "sphere":
            scene_obj = Sphere(np.array(geom_params["center"]), geom_params["radius"], **mat)
        elif obj["geometry"] == "cylinder":
            scene_obj = Cylinder(np.array(geom_params["center"]), geom_params["radius"], geom_params["h"], geom_params["v"], **mat)
        objects.append(scene_obj)
    return Scene(cam, light, objects)


def main():
    # Create a scene object
    scene = parse_scene("scene.json")

    # Create a renderer object with scene passed as param
    renderer = Renderer(scene, 3)

    # Call the renderer's render function
    im = renderer.render()
    im.save('img.png')


if __name__ == "__main__":
    main()
