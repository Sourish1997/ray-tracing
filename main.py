from scene.camera import Camera
from scene.point_light import PointLight
from scene.dir_light import DirLight
from scene.scene import Scene
from renderer import Renderer
from objects.sphere import Sphere
from objects.cylinder import Cylinder
from materials.base_material import BaseMaterial
import numpy as np
import json


def parse_scene_json(scene_json):
    """
    Param: scene_file - json file of scene description
    Returns: Scene obj to render
    """

    with open(scene_json, 'r') as scene_des:
        scene = json.loads(scene_des.read())['scene']

    # objects, lights, camera = scene['shapes'], scene['lights'], scene['camera']
    cam = Camera(**scene['camera'])

    lights = []
    for i in range(len(scene['lights'])):
        if scene['lights'][i]['type'] == 'point':
            lights.append(PointLight(**scene["lights"][i]))
        elif scene['lights'][i]['type'] == 'directional':
            lights.append(DirLight(**scene["lights"][i]))

    objects = []
    for obj in scene['shapes']:
        prop = obj["material"]
        mat = {"material": BaseMaterial(**prop)}
        geom_params = obj["geomParams"]
        if obj["geometry"] == "sphere":
            scene_obj = Sphere(np.array(geom_params["center"]), geom_params["radius"], **mat)
        elif obj["geometry"] == "cylinder":
            scene_obj = Cylinder(np.array(geom_params["center"]), geom_params["radius"], geom_params["h"], geom_params["v"], **mat)
        objects.append(scene_obj)
    return Scene(cam, lights, objects)


def main():
    # Create a scene object
    scene = parse_scene_json("scene.json")

    # Create a renderer object with scene passed as param
    renderer = Renderer(scene, 3)

    # Call the renderer"s render function
    im = renderer.render()
    im.save("img.png")


if __name__ == "__main__":
    main()
