import numpy as np
import math

# might want to add homogenous section?

class Vector:

    # Initalizes all necessary values
    def __init__(self, vector):
        # Gives us x, y, z values for the vectors
        self.x = vector[0]
        self.y = vector[1]
        self.z = vector[2]

        # Builds some necessary objects
        self.vector = vector
        self.cross_product = None
        self.normalized_vector = None
        self.dot_product = 0
        self.magnitude_vector = 0


    def __repr__(self):
        return "(" + str(self.x) + " " + str(self.y) + " " + str(self.z) + ")"
    # Returns a string in the format of a numpy array looking array
    def __str__(self):
        return "[" + str(self.x) + " " + str(self.y) + " " + str(self.z) + "]"

    # Has a custom check to see if vectors are equal
    def __eq__(self, vector2):
        if self.x == vector2.x and self.y == vector2.y and self.z == vector2.z:
            return True
        else:
            return False

    # Returns the negative of a vector
    def __neg__(self):
        self.vector = - self.vector

    def __mul__(self, other):
        new_vector = [self.x * other.x, self.y * other.y, self.z * other.z]
        return Vector(new_vector)


    def __truediv__(self, other):
        self.vector = [self.x / other, self.y / other, self.z / other]

    # Need to add mul and div functions

    # Adds two vectors together
    def __add__(self, other):
        new_vector = [self.x + other.x, self.y + other.y, self.z + other.z]
        return Vector(new_vector)

    def __sub__(self, other):
        new_vector = [self.x - other.x, self.y - other.y, self.z - other.z]
        return Vector(new_vector)

    # normalizes a vector
    def normalize(self):
        # Gets normalizing factor and divides each element by that and creates a new vector object from them
        normalize = self.magnitude()
        normalized_vector = (self.x / normalize, self.y/normalize, self.z/normalize)
        return Vector(normalized_vector)
        #self.normalized_vector = Vector([self.x, self.y, self.z])

    # will need to build a normal function as well

    # Cross product of two vectors
    def cross(self, vector2):
        # First builds two numpy arrays from the vectors so we can use np.cross and then converts back and normalizes
        vec1 = np.array(([self.x, self.y, self.z]))
        vec2 = np.array(([vector2.x, vector2.y, vector2.z]))
        cross_product = np.cross(vec1, vec2)
        if cross_product[0] == -0.0:
            cross_product[0] = 0.0
        if cross_product[1] == -0.0:
            cross_product[1] = 0.0
        if cross_product[2] == -0.0:
            cross_product[2] = 0.0
        self.cross_product = Vector(cross_product)
        self.cross_product.normalize()
        return self.cross_product

    def magnitude(self):
        magnitude_vector = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return magnitude_vector

    def to_array(self):
        vector_array = np.array(([self.x, self.y, self.z]))
        return vector_array

    # Dot product of two vectors
    def dot(self, vector2):
        self.dot_product = self.x * vector2.x + self.y * vector2.y + self.z * vector2.z
        return self.dot_product

    def to_homogenous(self):
        return np.array(([self.x, self.y, self.z, 1]))

    def scalar_mul(self, other):
        new_vector = [self.x * other, self.y * other, self.z * other]
        return Vector(new_vector)
