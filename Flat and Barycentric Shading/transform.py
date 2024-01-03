import math
import numpy as np
from vector import Vector

class Transform:

    def __init__(self):
        # Creates the necessary objects
        self.position = np.array([0, 0, 0])
        self.rotation_matrix = np.eye(4)
        self.transform_matrix = np.eye(4)
        self.inverse_transform_matrix = np.eye((4))

    # Just returns our transformation matrix
    def transformation_matrix(self):
        return self.transform_matrix

    # Sets the position of the point we may need to transform. First update the transform matrix with the necessary values
    # Then updates the position
    def set_position(self, x, y, z):
        self.transform_matrix[0][3] = x
        self.transform_matrix[1][3] = y
        self.transform_matrix[2][3] = z
        # Vector
        self.position = Vector([x, y, z])

        self.position = np.array([x, y, z])

    # Defines each rotation matrix depending on which axis we are rotating about. Then gets all of the rotation matrices
    def rotation(self, x, y, z):

        rotation_x = np.array(
                            ([1, 0, 0, 0],
                            [0, math.cos(x), -math.sin(x), 0],
                            [0, math.sin(x), math.cos(x), 0],
                            [0, 0, 0, 1]))

        rotation_y = np.array(
                            ([math.cos(y), 0, math.sin(y), 0],
                            [0, 1, 0, 0],
                            [-math.sin(y), 0, math.cos(y), 0],
                            [0, 0, 0, 1]))
        rotation_z = np.array(
                            ([math.cos(z), -math.sin(z), 0, 0],
                            [math.sin(z), math.cos(z), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]))

        self.rotation_matrix = np.matmul(rotation_x, np.matmul(rotation_y, rotation_z))

    # Sets the rotation based on the given x, y, z
    def set_rotation(self, x, y, z):
        x = np.deg2rad(x)
        y = np.deg2rad(y)
        z = np.deg2rad(z)

        # define x, y, z rotation matrices, then multiply together by calling this rotation method
        self.rotation(x, y, z)

        # Updates our transformation matrix
        self.transform_matrix = np.matmul(self.transform_matrix, self.rotation_matrix)

    # Gets the inverse of the transformation matrix
    def inverse_matrix(self):
        self.inverse_transform_matrix = np.linalg.inv(self.transform_matrix)
        return self.inverse_transform_matrix

        # Applies the transformation matrix to a point and converts to the necessary homogenous cords
    def apply_to_point(self, p):
        homogenous_p = np.append(p, 1)
        homogenous_p_prime = np.matmul(self.transform_matrix, homogenous_p)
        if homogenous_p_prime[3]!= 0:
            p_prime = np.array((homogenous_p_prime[0]/homogenous_p_prime[3], homogenous_p_prime[1]/homogenous_p_prime[3], homogenous_p_prime[2]/homogenous_p_prime[3]))
        else:
            p_prime = np.array(homogenous_p_prime[0], homogenous_p_prime[1], homogenous_p_prime[2])
        return p_prime

        # Does the same as apply to point, except with the inverse transformation matrix
    def apply_inverse_to_point(self, p):
        homogenous_p = np.append(p, 1)
        self.inverse_transform_matrix = self.inverse_matrix()
        homogenous_p_prime = np.matmul(self.inverse_transform_matrix, homogenous_p)
        if homogenous_p_prime[3]!= 0:
            p_prime = np.array((homogenous_p_prime[0]/homogenous_p_prime[3], homogenous_p_prime[1]/homogenous_p_prime[3], homogenous_p_prime[2]/homogenous_p_prime[3]))
        else:
            p_prime = np.array((homogenous_p_prime[0], homogenous_p_prime[1], homogenous_p_prime[2]))
        return p_prime

    # Takes a normal vector and applies the rotation matrix to it
    def apply_to_normal(self, n):
        n_homogenous = np.append(n, 1)
        homogenous_n_prime = np.matmul(self.rotation_matrix, n_homogenous)
        if n_homogenous[3]!= 0:
            n_prime = np.array((homogenous_n_prime[0]/n_homogenous[3], homogenous_n_prime[1]/homogenous_n_prime[3], homogenous_n_prime[2]/homogenous_n_prime[3]))
        else:
            n_prime = np.array((homogenous_n_prime[0], homogenous_n_prime[1], homogenous_n_prime[2]))
        return n_prime


    # Takes in a rotation amount and the rotation axis and updates our rotation and transformation matrices. Basically does what
    # self.rotation is doing.
    def set_axis_rotation(self, axis, rotation):
        rotation = np.deg2rad(rotation)
        rotation_matrix = axis * rotation
        self.rotation(rotation_matrix.item(0), rotation_matrix.item(1), rotation_matrix.item(2))
        self.transform_matrix = np.matmul(self.transform_matrix, self.rotation_matrix)
