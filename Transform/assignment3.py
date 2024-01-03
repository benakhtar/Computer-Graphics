import numpy as np

from mesh import Mesh
from transform import Transform


def transform_cube():
    # I am very confused by this and the whole mesh class and why you are using static methods
    mesh = Mesh.from_stl("unit_cube.stl")

    # Don't forget to add a Transform member to Mesh
    mesh.transform.set_position(1.0, 2.0, 3.0)
    mesh.transform.set_rotation(45.0, 0.0, 45.0)

    for vert in mesh.verts:
        print(mesh.transform.apply_to_point(vert))

def test_x_rotation_matrix():
    rot = 30 # degrees
    transform = Transform()
    transform.set_rotation(rot, 0.0, 0.0)

    # Test to see if correct rotation matrix was calculated
    assert np.allclose(transform.transformation_matrix(), np.array([
        [1.,         0.,         0.,         0.],
        [0.,         0.8660254, -0.5,        0.],
        [0.,         0.5,        0.8660254,  0.],
        [0.,         0.,         0.,         1.]
    ]))



def test_y_rotation_matrix():
    rot = 30  # degrees
    transform = Transform()
    transform.set_rotation(0.0, rot, 0.0)

    # Test to see if correct rotation matrix was calculated
    assert np.allclose(transform.transformation_matrix(), np.array([
        [ 0.8660254,   0.,         0.5,        0.],
        [ 0.,          1.,         0.,         0.],
        [-0.5,         0.,         0.8660254,  0.],
        [ 0.,          0.,         0.,         1.]
    ]))



def test_z_rotation_matrix():
    rot = 30  # degrees
    transform = Transform()
    transform.set_rotation(0.0, 0.0, rot)

    # Test to see if correct rotation matrix was calculated
    assert np.allclose(transform.transformation_matrix(), np.array([
        [0.8660254,   -0.5,               0.,         0.],
        [0.5,          0.8660254,         0.,         0.],
        [0,            0.,                1.,         0.],
        [0.,           0.,                0.,         1.]
    ]))


def test_set_position():
    transform = Transform()
    transform.set_position(1, 2, 3)

    # Test to make sure position was set correctly
    assert np.allclose(transform.transformation_matrix()[0:3, 3], np.array([1, 2, 3]))

    transform.set_position(4, 5, 6)

    # Test to make sure position was set correctly (reset, not added to
    assert np.allclose(transform.transformation_matrix()[0:3, 3], np.array([4, 5, 6]))

    # Test to make sure that setting position doesn't affect rotation
    assert np.allclose(transform.transformation_matrix()[0:3, 0:3], np.identity(3))


def test_inverse_matrix():
    transform = Transform()

    # Test that empty transform (identity) has identity inverse
    assert np.allclose(transform.inverse_matrix(), np.identity(4))

    transform.set_rotation(45, 0, 45)
    transform.set_position(1, 2, 3)

    # Test inverse after rotation and position have been set
    assert np.allclose(transform.inverse_matrix(), np.array([
        [ 0.70710678,  0.5,         0.5,        -3.20710678],
        [-0.70710678,  0.5,         0.5,        -1.79289322],
        [ 0.,         -0.70710678,  0.70710678, -0.70710678],
        [ 0.,          0.,          0.,          1.],
    ]))


def test_apply_to_point():
    transform = Transform()
    transform.set_position(1, 2, 3)

    # Test just translation
    assert np.allclose(transform.apply_to_point(np.zeros((1, 3))), np.array([1, 2, 3]))

    p = np.array([1, 2, 3])
    transform = Transform()
    transform.set_rotation(55, 0, 0)

    # Test just rotation
    assert np.allclose(transform.apply_to_point(p), np.array([1.0, -1.3103032601648832, 3.359033397631122]))

    transform.set_position(1, 2, 3)

    # Test both translation and rotation
    assert np.allclose(transform.apply_to_point(p), np.array([2.0, 0.6896967398351168, 6.359033397631122]))


def test_apply_inverse_to_point():
    transform = Transform()
    transform.set_position(1, 2, 3)

    # Test just translation
    assert np.allclose(transform.apply_inverse_to_point(np.zeros((1, 3))), np.array([-1, -2, -3]))

    p = np.array([1, 2, 3])
    transform = Transform()
    transform.set_rotation(55, 0, 0)

    # Test just rotation
    assert np.allclose(transform.apply_inverse_to_point(p), np.array([1.0, 3.6046090055690674, 0.08242522047515455]))

    transform.set_position(1, 2, 3)

    # Test both translation and rotation
    assert np.allclose(transform.apply_inverse_to_point(p), np.array([0.0, 0.0, 0.0]))


def test_apply_to_normal():
    n = np.array([1, 2, 3])
    n_mag = np.sqrt(np.sum(np.power(n, 2)))
    n = n / n_mag

    transform = Transform()
    transform.set_position(1, 2, 3)

    # Test just translation (should not affect normal rotation)
    assert np.allclose(transform.apply_to_normal(n), n)


    transform = Transform()
    transform.set_rotation(55, 0, 0)

    # Test just rotation
    assert np.allclose(transform.apply_to_normal(n), np.array([0.2672612419124244, -0.35019327659356525, 0.8977394374762041]))

    transform.set_position(1, 2, 3)

    # Test both translation and rotation (again, the position shouldn't affect normal rotation)
    assert np.allclose(transform.apply_to_normal(n), np.array([0.2672612419124244, -0.35019327659356525, 0.8977394374762041]))

if __name__ == '__main__':
    transform_cube()




