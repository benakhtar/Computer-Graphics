import math
from transform import Transform
from stl import mesh as mesh_import
from vector import Vector


class Mesh:

    def __init__(self):
        # Inits our structures
        self.normals = []
        self.triangles = None
        self.faces = []
        self.verts = []
        self.transform = Transform()

    @staticmethod
    def from_stl(stl_path):
        # Loads in our stl file
        stl_mesh = mesh_import.Mesh.from_file(stl_path)
        mesh = Mesh()
        # This gives us a list of the triangles/their vertices
        mesh.triangles = stl_mesh.vectors

        mesh.faces = []
        mesh.verts = []
        mesh.normals = []

        # Counters used for faces
        index = 0
        count = 0
        indexes = []

        # Overall for loop. We check to see if the vertex is already in our list. If not, add it, increase index
        # by 1. If it is, determine where it is (get the index). We will add each index to an indexes array
        # that will take each indexes list at the end of each triangle loop and add it to the self.faces
        # We also add the vertices if not already in our numpy list to self.verts

        for triangle in mesh.triangles:
            for vertex in triangle:
                # If list is empty, need to add first entry, otherwise, check next statement
                if not mesh.verts:
                    vertex = tuple(vertex)
                    mesh.verts.append(vertex)
                    indexes.append(index)
                    index += 1
                # Checks to see if vertex already in the list
                elif (vertex == mesh.verts).all(1).any():
                    # Finds the index of where it exists
                    verts_index_list = (mesh.verts == vertex).all(axis=1).nonzero()
                    # Removes any data types to get the int
                    verts_index= verts_index_list[0][0]
                    indexes.append(verts_index)
                else:
                    # Add the vertex to necessary arrays and increase index by 1
                    vertex = tuple(vertex)
                    mesh.verts.append(vertex)
                    indexes.append(index)
                    index += 1
            # Add indexes array to faces
            mesh.faces.append(indexes)
            count += 1
            indexes = []

        # Calculate the self.normals values
        mesh.calculate_normals()

        return mesh


    # This method calculates our normals
    # It uses the 3 vertices from the self.triangles method, crosses the 2 vectors that are created by
    # setting our anchor at one point and going to the other 2.

    def calculate_normals(self):
        for vertex in range (0, len(self.triangles)):
            vertex_1 = Vector(self.triangles[vertex][0])
            vertex_2 = Vector(self.triangles[vertex][1])
            vertex_3 = Vector(self.triangles[vertex][2])
            vector_1 = vertex_1 - vertex_2
            vector_2 = vertex_1-vertex_3
            normal   = vector_1.cross(vector_2)

            self.normals.append(normal)