import numpy as np

from mesh import Mesh
from transform import Transform
from camera import OrthoCamera

def ortho_camera():
    mesh = Mesh.from_stl("unit_cube.stl")
    mesh.transform.set_rotation(-45, -45, 45)
   
    camera = OrthoCamera(1.5, -1.5, -1.5, 1.5, -1, -50)
    camera.transform.set_position(0, 5, 0)

    verts = [camera.project_point(p) for p in mesh.verts]

    #test unit cube in model space 
    for vert in verts:
        print(vert)

    #test camera coordinate system transform
    verts = [camera.transform.apply_inverse_to_point(p) for p in mesh.verts]

    for vert in verts:
        print(vert)

    #test unit cube in world space
    verts = [camera.project_point(mesh.transform.apply_to_point(p)) for p in mesh.verts]

    for vert in verts:
        print(vert)


def test_point():
    camera = OrthoCamera(1.5, -1.5, -1.5, 1.5, -1, -50)
    camera.transform.set_position(0,3,0)

    #Test just camera translation
    assert np.allclose(camera.project_point(np.array([0,-2,1])),np.array([0.0, 0.6666666666666666, 0.8367346938775511]))

    camera = OrthoCamera(2.5, -2.5, -1.5, 1.5, -1, -50)
    camera.transform.set_rotation(0.0,30.0,0.0)

    #Test just camera rotation
    assert np.allclose(camera.project_point(np.array([0,-2,1])),np.array([0.19999999999999998, 0.5773502691896257, 0.9591836734693878]))

    camera = OrthoCamera(3.5, -3.5, -2.5, 2.5, -1, -50)
    camera.transform.set_position(0,3,0)
    camera.transform.set_rotation(0.0,30.0,0.0)

    #Test camera translation and rotation
    assert np.allclose(camera.project_point(np.array([0,-2,1])),np.array([0.14285714285714282, 0.3464101615137755, 0.8367346938775511]))

def test_inverse_point():
    camera = OrthoCamera(1.5, -1.5, -1.5, 1.5, -1, -50)
    camera.transform.set_position(0,3,0)

    #Test just camera translation
    assert np.allclose(camera.inverse_project_point(np.array([0.5,0.5,1.0])),np.array([-0.75, 2.0, 0.75]))

    camera = OrthoCamera(2.5, -2.5, -1.5, 1.5, -1, -50)
    camera.transform.set_rotation(0.0,30.0,0.0)

    #Test just camera rotation
    assert np.allclose(camera.inverse_project_point(np.array([0.5,0.5,1.0])),np.array([-0.7075317547305484, -1.0, 1.274519052838329]))

    camera = OrthoCamera(3.5, -3.5, -2.5, 2.5, -1, -50)
    camera.transform.set_position(0,3,0)
    camera.transform.set_rotation(0.0,30.0,0.0)

    #Test camera translation and rotation
    assert np.allclose(camera.inverse_project_point(np.array([0.5,0.5,1.0])),np.array([-0.8905444566227679, 2.0, 1.9575317547305482]))
    
def test_ratio():
    from math import isclose

    camera = OrthoCamera(1.5, -1.5, -1.5, 1.5, -1, -50)
    assert isclose(camera.ratio(), 1.0)

    camera = OrthoCamera(3.5, -3.5, -2.5, 2.5, -1, -50)
    assert isclose(camera.ratio(), 1.4)

if __name__ == '__main__':
    ortho_camera()





