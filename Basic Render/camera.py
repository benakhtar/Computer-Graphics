from transform import Transform
import numpy as np
from vector import Vector
import math

# Will want to discuss the perspective matrix and some of the ops after getting the points back

class OrthoCamera:

    def __init__(self, left, right, bottom, top, near, far):
        self.left   = left
        self.right  = right
        self.top    = top
        self.bottom = bottom
        self.near   = near
        self.far    = far
        self.width  = self.left - self.right
        self.height = self.top  - self.bottom
        self.depth  = self.near - self.far

        # Creates our ortho_transform array, with our correct flipping
        self.ortho_transform = np.array((
            [2 / -self.width, 0, 0, - ((self.left + self.right)/-self.width)],
            [0, 2 / self.depth, 0, - ((self.far + self.near) / self.depth)],
            [0, 0, 2 / self.height, - ((self.top + self.bottom) / self.height)],
            [0, 0, 0, 1]
        ))
        # Builds the inverse array
        self.inverse_ortho_transform = np.linalg.inv(self.ortho_transform)

        self.transform = Transform()

    def ratio(self):
        # Creates a correct return of our return (do not want this to be negative)
        return abs(self.width/self.height)

    def project_point(self, p):

        # Apply the inverse so the camera is shifted to the origin
        camera_point = self.transform.apply_inverse_to_point(p)
        # Turns this into a vector
        camera_point = Vector(camera_point)
        # Turns it into a homogenous cordinate
        camera_point = camera_point.to_homogenous()

        # Applies our ortho matrix
        ortho_point  = np.matmul(self.ortho_transform, camera_point)

        # Removes the fourth cordinate
        ortho_point  = self.to_three_d(ortho_point)
        # Returns our normalized point
        ortho_point = [ortho_point[0], ortho_point[2], ortho_point[1]]
        return ortho_point

    def inverse_project_point(self, p):
        # Creates a numpy array with the points being flipped as necessary
        p = np.array((p[0], p[2], p[1], 1))
        # applies the inverse of the ortho transform
        world_point = np.matmul(self.inverse_ortho_transform, p)

        # Gets our point in 3-D
        world_point = self.to_three_d(world_point)
        # Applies the transform to get it back to the world cords
        world_point = self.transform.apply_to_point(world_point)
        return world_point

    def to_homogenous(self, point):
        return np.append(point, 1)

    def to_three_d(self, point):
        if point[3]!= 0:
            three_d_point = np.array((point[0]/point[3], point[1]/point[3], point[2]/point[3]))
        else:
            three_d_point = np.array((point[0], point[1], point[2]))
        return three_d_point


class PerspectiveCamera:

    # basically just need to add self.perspective_transform

    def __init__(self, left, right, bottom, top, near, far):
        self.left   = left
        self.right  = right
        self.top    = top
        self.bottom = bottom
        self.near   = near
        self.far    = far
        self.width  = self.left - self.right
        self.height = self.top  - self.bottom
        self.depth  = self.near - self.far

        # Creates our ortho_transform array, with our correct flipping
        self.ortho_transform = np.array((
            [2 / -self.width, 0, 0, - ((self.left + self.right)/-self.width)],
            [0, 2 / self.depth, 0, - ((self.far + self.near) / self.depth)],
            [0, 0, 2 / self.height, - ((self.top + self.bottom) / self.height)],
            [0, 0, 0, 1]
        ))
        # Builds the inverse array
        self.inverse_ortho_transform = np.linalg.inv(self.ortho_transform)

        self.transform = Transform()

        # Gets our perspective transform
        self.perspective_transform = np.array((
            [-self.near, 0, 0, 0],
            [0, (self.near + self.far), 0, -(self.near * self.far)],
            [0, 0, self.near, 0],
            [0, 1, 0, 0]))
        # Gets our perspective transform inverse
        self.inverse_perspective_transform = np.linalg.inv(self.perspective_transform)

    def ratio(self):
        # Creates a correct return of our return (do not want this to be negative)
        return abs(self.width/self.height)

    def project_point(self, p):

        # Apply the inverse so the camera is shifted to the origin
        camera_point = self.transform.apply_inverse_to_point(p)
        # Turns this into a vector
        camera_point = Vector(camera_point)
        # Turns it into a homogenous cordinate
        camera_point = camera_point.to_homogenous()
        # applies perspective matrix
        perspective_point = np.matmul(self.perspective_transform, camera_point)
        # Applies our ortho matrix
        ortho_point  = np.matmul(self.ortho_transform, perspective_point)

        # Removes the fourth cordinate by dividing by y
        ortho_point  = self.to_three_d(ortho_point)
        # Returns our normalized point
        ortho_point = [ortho_point[0], ortho_point[2], ortho_point[1]]
        return ortho_point

    def project_inverse_point(self, p):
        # Creates a numpy array with the points being flipped as necessary
        p = np.array((p[0], p[2], p[1], 1))
        # applies the inverse of perspective transform
        perspective_point = np.matmul(self.inverse_ortho_transform, p)
        # applies the inverse of the ortho transform
        world_point = np.matmul(self.inverse_perspective_transform, perspective_point)

        # Gets our point in 3-D
        world_point = self.to_three_d(world_point)
        # Applies the transform to get it back to the world cords
        world_point = self.transform.apply_to_point(world_point)
        return world_point

    # This should be good?
    @staticmethod
    def from_FOV(fov, near, far, ratio):
        pass
        #assume that left and right are symmetric
        #assume that top and bottom are symmetric
        # have horizontal field of view in degrees
        # have near, far
        # have the ratio

        # change from degress to radians

        # Changes to radians then calculates width and height
        fov = np.deg2rad(fov)
        width  = abs(2 * near * np.tan((fov / 2))) # don't use far - near here, interesting
        height = width / ratio

        # Builds our attributes and then builds PerspectiveCamera
        top    = height / 2
        bottom = - (height / 2)
        right  = - (width / 2)
        left   = width / 2
        camera = PerspectiveCamera(left, right, bottom, top, near, far)

        # returns our camera object
        return camera


    def to_homogenous(self, point):
        return np.append(point, 1)

    def to_three_d(self, point):
        if point[3]!= 0:
            three_d_point = np.array((point[0]/point[3], point[1]/point[3], point[2]/point[3]))
        else:
            three_d_point = np.array((point[0], point[1], point[2]))
        return three_d_point



