from scene.camera import Camera
from scene.light import Light
from scene.scene import Scene
from renderer import Renderer
from objects.sphere import Sphere
from objects.cylinder import Cylinder
from objects.plane import Plane
from objects.triangle import Triangle
# from objects.cone import Cone
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
    u = np.array(scene["camera"]["u"])
    v = np.array(scene["camera"]["v"])
    fov = math.pi / scene["camera"]["fov"]
    cam = Camera(cam_from, cam_to, u, v, fov, width, height)

    # TODO: light (only support for point lights rn, requires refactoring of light.py)
    light = []
    for i in range(len(scene["lights"])):
        light.append(Light(**scene["lights"][i]))

    objects = []
    for obj in scene["shapes"]:
        prop = obj["material"]
        mat = {"material": BaseMaterial(**prop)}
        geom_params = obj["geomParams"]
        if obj["geometry"] == "sphere":
            scene_obj = Sphere(np.array(geom_params["center"]), geom_params["radius"], **mat)
        elif obj["geometry"] == "cylinder":
            scene_obj = Cylinder(np.array(geom_params["center"]), geom_params["radius"], geom_params["h"], geom_params["v"], **mat)
        elif obj["geometry"] == "plane":
            scene_obj = Plane(np.array(geom_params["point0"]), np.array(geom_params["normal"]), **mat)
        elif obj["geometry"] == "triangle":
            scene_obj = Triangle(np.array(geom_params["v0"]), np.array(geom_params["v1"]), np.array(geom_params["v2"]), **mat)
        # elif obj["geometry"] == "cone":
        #     scene_obj = Cone(np.array(geom_params["pA"]), np.array(geom_params["p1"]), geom_params["r1"], **mat)
        objects.append(scene_obj)
    return Scene(cam, light, objects)


def main():
    # Create a scene object
    scene = parse_scene_json("scene1.json")

    # Create a renderer object with scene passed as param
    renderer = Renderer(scene, 3)

    # Call the renderer"s render function
    im = renderer.render()
    im.save("img1.png")


if __name__ == "__main__":
    main()
