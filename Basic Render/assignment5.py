import numpy as np

from camera import PerspectiveCamera
from mesh import Mesh



def test_perspective_points():
    camera = PerspectiveCamera(1.5, -1.5, -1.5, 1.5, -1, -100)
    camera.transform.set_position(0, 60, 0)

    mesh = Mesh.from_stl("unit_cube.stl")
    mesh.transform.set_rotation(0, 0, 0)

    verts_world = [mesh.transform.apply_to_point(p) for p in mesh.verts]
    verts_screen = [camera.project_point(p) for p in verts_world]

    verts_correct = [
        np.array([0.00560224, 0.00560224, -0.98624905]),
        np.array([-0.00560224, 0.00560224, -0.98624905]),
        np.array([-0.00550964, 0.00550964, -0.98681025]),
        np.array([0.00550964, 0.00550964, -0.98681025]),
        np.array([0.00550964, -0.00550964, -0.98681025]),
        np.array([-0.00550964, -0.00550964, -0.98681025]),
        np.array([-0.00560224, -0.00560224, -0.98624905]),
        np.array([0.00560224, -0.00560224, -0.98624905])
    ]

    for v1 in verts_screen:
        found = False
        for v2 in verts_correct:
            if np.allclose(v1, v2):
                found = True
                break

        assert found

def test_perspective_inverse():
    from pprint import pprint

    camera = PerspectiveCamera(1.5, -1.5, -1.5, 1.5, -1, -100)
    camera.transform.set_position(0, 60, 0)

    mesh = Mesh.from_stl("unit_cube.stl")
    mesh.transform.set_rotation(0, 0, 0)

    verts_world = [mesh.transform.apply_to_point(p) for p in mesh.verts]
    verts_screen = [camera.project_point(p) for p in verts_world]
    verts_screen_inverse = [camera.project_inverse_point(p) for p in verts_screen]

    assert np.allclose(verts_world, verts_screen_inverse)