from mesh import Mesh
from pprint import pprint

def test_from_stl():
    mesh = Mesh()
    mesh.from_stl("unit_cube.stl")
    #mesh = Mesh.from_stl("unit_cube.stl")

def test_list_sizes():
    mesh = Mesh()
    mesh.from_stl("unit_cube.stl")
    #mesh = Mesh.from_stl("unit_cube.stl")

    assert len(mesh.verts) == 8
    assert len(mesh.faces) == 12
    assert len(mesh.normals) == 12

if __name__ == '__main__':
    mesh = Mesh()
    mesh.from_stl("unit_cube.stl")

    #mesh = Mesh.from_stl("unit_cube.stl")

    pprint(mesh.verts)
    pprint(mesh.faces)
    pprint(mesh.normals)
