import numpy as np

from transform import Transform

def test_x_rotation_matrix():
    rot = 30 # degrees
    transform = Transform()
    transform.set_axis_rotation(np.array([1.0, 0.0, 0.0]), rot)

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
    transform.set_axis_rotation(np.array([0.0, 1.0, 0.0]), rot)

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
    transform.set_axis_rotation(np.array([0.0, 0.0, 1.0]), rot)

    # Test to see if correct rotation matrix was calculated
    assert np.allclose(transform.transformation_matrix(), np.array([
        [0.8660254,   -0.5,               0.,         0.],
        [0.5,          0.8660254,         0.,         0.],
        [0,            0.,                1.,         0.],
        [0.,           0.,                0.,         1.]
    ]))