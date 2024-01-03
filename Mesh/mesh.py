import numpy

from stl import mesh as ben


class Mesh:

    def __int__(self):
        # Inits our structures
        self.normals = []
        self.triangles = None
        self.faces = []
        self.verts = []

    def from_stl(self, stl_path):
        # Loads in our stl file
        stl_mesh = ben.Mesh.from_file(stl_path)

        # This gives us a list of the triangles/their vertices
        self.triangles = stl_mesh.vectors

        self.faces = []
        self.verts = []
        self.normals = []

        # Counters used for faces
        index = 0
        count = 0
        indexes = []

        # Overall for loop. We check to see if the vertex is already in our list. If not, add it, increase index
        # by 1. If it is, determine where it is (get the index). We will add each index to an indexes array
        # that will take each indexes list at the end of each triangle loop and add it to the self.faces
        # We also add the vertices if not already in our numpy list to self.verts

        for triangle in self.triangles:
            for vertex in triangle:
                # If list is empty, need to add first entry, otherwise, check next statement
                if not self.verts:
                    vertex = tuple(vertex)
                    self.verts.append(vertex)
                    indexes.append(index)
                    index += 1
                # Checks to see if vertex already in the list
                elif (vertex == self.verts).all(1).any():
                    # Finds the index of where it exists
                    verts_index_list = (self.verts == vertex).all(axis=1).nonzero()
                    # Removes any data types to get the int
                    verts_index= verts_index_list[0][0]
                    indexes.append(verts_index)
                else:
                    # Add the vertex to necessary arrays and increase index by 1
                    vertex = tuple(vertex)
                    self.verts.append(vertex)
                    indexes.append(index)
                    index += 1
            # Add indexes array to faces
            self.faces.append(indexes)
            count += 1
            indexes = []

        # Calculate the self.normals values
        self.calculate_normals()


    # This method calculates our normals
    # It uses the 3 vertices from the self.triangles method, crosses the 2 vectors that are created by
    # setting our anchor at one point and going to the other 2.
    def calculate_normals(self):
        for vertex in range (0, len(self.triangles)):
            vertex_1 = self.triangles[vertex][0]
            vector_1 = vertex_1 - self.triangles[vertex][1]
            vector_2 = vertex_1 - self.triangles[vertex][2]
            normal = self.cross_product(vector_1, vector_2)
            self.normals.append(normal)


    # This gets our cross product from our two vectors for each triangle. We also make sure to set -0.0 to 0.0
    def cross_product(self, vector_1, vector_2):
        normal_x = vector_1[1] * vector_2[2] - vector_2[1] * vector_1[2]
        normal_y = vector_2[0] * vector_1[2] - vector_1[0] * vector_2[2]
        normal_z = vector_1[0] * vector_2[1] - vector_2[0] * vector_1[1]
        if normal_x == -0.0:
            normal_x = 0.0
        if normal_y == -0.0:
            normal_y = 0.0
        if normal_z == -0.0:
            normal_z = 0.0
        return normal_x, normal_y, normal_z