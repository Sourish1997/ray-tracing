from scene.camera import Camera
from scene.point_light import PointLight
from scene.dir_light import DirLight
from scene.scene import Scene
from renderer import Renderer
from objects.sphere import Sphere
from objects.cylinder import Cylinder
from objects.cuboid import Cuboid
from objects.plane import Plane
from objects.triangle import Triangle
from objects.cone import Cone
from materials.ref_blinn_material import RefBlinnMaterial
from materials.transmissive_material import TransmissiveMaterial
from materials.path_blinn_material import PathBlinnMaterial
from materials.reflective_material import ReflectiveMaterial
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
            lights.append(PointLight(**scene['lights'][i]))
        elif scene['lights'][i]['type'] == 'directional':
            lights.append(DirLight(**scene['lights'][i]))

    objects = []
    for obj in scene['shapes']:
        kwargs = obj['geomParams']
        if obj['mat_type'] == 'base':
            obj_type = RefBlinnMaterial
        elif obj['mat_type'] == 'transmissive':
            obj_type = TransmissiveMaterial
        elif obj['mat_type'] == 'reflective':
            obj_type = ReflectiveMaterial
        elif obj['mat_type'] == 'path_blinn':
            obj_type = PathBlinnMaterial

        kwargs.update({'material': obj_type(**obj['material'])})
        if obj['geometry'] == 'sphere':
            scene_obj = Sphere(**kwargs)
        elif obj['geometry'] == 'cylinder':
            scene_obj = Cylinder(**kwargs)
        elif obj['geometry'] == 'plane':
            scene_obj = Plane(**kwargs)
        elif obj['geometry'] == 'triangle':
            scene_obj = Triangle(**kwargs)
        elif obj['geometry'] == 'cone':
            scene_obj = Cone(**kwargs)
        elif obj['geometry'] == 'cuboid':
            scene_obj = Cuboid(**kwargs)
        objects.append(scene_obj)
    return Scene(cam, lights, objects)


def main():
    # Create a scene object
    scene = parse_scene_json('ref.json')

    # Create a renderer object with scene passed as param
    renderer = Renderer(scene, 2)

    # Call the renderer's render function
    im, o_im, f_im = renderer.render(8)
    im.save('ref.png')
    # o_im.save('o_img.png')  # Comment this out if you pass False as the occlusion parameter to renderer()
    # f_im.save('f_img.png')  # Comment this out if you pass False as the occlusion parameter to renderer()


if __name__ == '__main__':
    main()
