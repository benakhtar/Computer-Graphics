import math
from transform import Transform
from stl import mesh as mesh_import
from vector import Vector
import numpy as np
from PIL import Image


class Mesh:

    def __init__(self, diffuse_color = 0, specular_color = 0, ka = 0, kd = 0, ks = 0, ke = 0):
        # add = 0 for all of these
        # Inits our structures
        self.normals = []
        self.triangles = None
        self.faces = []
        self.verts = []
        self.vertex_normals = []
        self.transform = Transform()

        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.ke = ke

        self.specular_color = specular_color
        self.diffuse_color  = diffuse_color

        self.uvs = []
        self.texture = []

    @staticmethod
    def from_stl(stl_path, diffuse_color, specular_color, ka, kd, ks, ke):
        # Loads in our stl file
        stl_mesh = mesh_import.Mesh.from_file(stl_path)
        mesh = Mesh(diffuse_color, specular_color, ka, kd, ks, ke)
        # This gives us a list of the triangles/their vertices
        mesh.triangles = stl_mesh.vectors

        mesh.faces = []
        mesh.verts = []
        mesh.vertex_normals = []
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
        mesh.calculate_vertex_normals()

        return mesh



    def sphere_uvs(self):
        uvs = []
        verts = self.verts

        # loop over each vertex
        for v in verts:
            # convert cartesian to spherical
            uv = self.cart2sph(v)

            # convert theta and phi to u and v by normalizing angles
            uv[0] += np.pi
            uv[1] += np.pi / 2.0

            uv[0] /= 2.0 * np.pi
            uv[1] /= np.pi

            uvs.append(uv)

        self.uvs = uvs

        return uvs

    def cart2sph(self, v):
        x = v[0]
        y = v[1]
        z = v[2]

        theta = np.arctan2(y, x)
        phi = np.arctan2(z, np.sqrt(x ** 2 + y ** 2))
        return np.array([theta, phi])

    @staticmethod
    def textured_quad():
        mesh = Mesh()
        # mesh.verts = [np.array([0.4, 0.5, -0.5]),
        #     np.array([-0.4, 0.5, -0.4]),
        #     np.array([0.4, -0.5, 0.4]),
        #     np.array([-0.4, -0.9, 0.4])
        #     ]

        mesh.verts = [np.array([0.4, 0.5, -0.5]),
                      np.array([-0.4, 0.5, -0.5]),
                      np.array([0.5, -0.5, 0.4]),
                      np.array([-0.4, -0.55, 0.4])
                      ]

        mesh.faces = [[0, 1, 2], [3, 2, 1]]

        mesh.triangles = []

        for tri in range(0, len(mesh.faces)):
            face = mesh.faces[tri]
            vert_1 = face[0]
            vert_2 = face[1]
            vert_3 = face[2]

            vertices = [mesh.verts[vert_1], mesh.verts[vert_2], mesh.verts[vert_3]]
            mesh.triangles.append(vertices)
        # todo: once happy, print the normals and set manually to avoid dependency on vector3 class
        normals = []
        for face in mesh.faces:
            a = Vector(mesh.verts[face[0]])
            b = Vector(mesh.verts[face[1]])
            c = Vector(mesh.verts[face[2]])
            n = Vector.cross(b - a, c - a)

            n = n.normalize()

            normals.append(n)
        mesh.calculate_normals()
        mesh.calculate_vertex_normals()

        mesh.uvs = [np.array([0.0,0.0]),np.array([1.0,0.0]),np.array([0.0,1.0]),np.array([1.0,1.0])]

        return mesh

    def load_texture(self, img_path):
        self.texture = np.asarray(Image.open(img_path), dtype ="int32")

    # This method calculates our normals
    # It uses the 3 vertices from the self.triangles method, crosses the 2 vectors that are created by
    # setting our anchor at one point and going to the other 2.

    def calculate_normals(self):
        for vertex in range (0, len(self.triangles)):
            vertex_1 = Vector(self.triangles[vertex][0])
            vertex_2 = Vector(self.triangles[vertex][1])
            vertex_3 = Vector(self.triangles[vertex][2])
            vector_1 = vertex_1 - vertex_2
            vector_2 = vertex_1 - vertex_3
            normal   = vector_1.cross(vector_2)
            normal = normal.normalize()
            self.normals.append(normal)

    # QUESTION correct way to calc normals?
    def calculate_vertex_normals(self):
        # Loops through each vertex in self.verts
        for vertex in range(0, len(self.verts)):
            # resets some counters
            vertex_normals_x = 0.0
            vertex_normals_y = 0.0
            vertex_normals_z = 0.0
            num_faces = 0
            # loops through each face in self.faces
            for face in range(0, len(self.faces)):
                # If our vertex is in self.faces current, we then add the x, y, z components to our normal and then will
                # increment the number of faces involved in this vector by 1
                if vertex in self.faces[face]:
                    vertex_normals_x += self.normals[face].x
                    vertex_normals_y += self.normals[face].y
                    vertex_normals_z += self.normals[face].z
                    num_faces += 1
            # gets our vertex norm for this vertex and creates a vector out of it
            vertex_normal = np.array((vertex_normals_x / num_faces, vertex_normals_y / num_faces, vertex_normals_z / num_faces))
            vertex_normal = Vector(vertex_normal).normalize()
            self.vertex_normals.append(vertex_normal)




