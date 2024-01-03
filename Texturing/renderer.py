from screen import Screen
from camera import PerspectiveCamera
from mesh import Mesh
import numpy as np
from vector import Vector
import math

class Renderer:

    def __init__(self, screen, camera, meshes, light):
        self.screen = screen
        self.camera = camera
        self.meshes = meshes
        self.light  = light
        self.mesh   = meshes[0]

        self.endpoint_1_color = (255, 0, 0)
        self.endpoint_2_color = (0, 255, 0)
        self.endpoint_3_color = (0, 0, 255)

        #self.z_buffer_value = - 1000000000000000000000
        self.z_buffer = np.full((self.screen.height, self.screen.width), -1000000000000000000000.00)

    def render(self, shading, bg_color, ambient_light):

        # define a screen and background/foreground colors for silhouette
        bg_color = bg_color
        image_buffer = np.full((self.screen.height, self.screen.width, 3), bg_color)

        # Gets camera position and normalizes it
        cam = Vector(self.camera.transform.position).normalize()
        cam_world = Vector(self.camera.transform.position)

        uvs = []

        for self.mesh in self.meshes:
            # change the cordintates to device cords for each vert
            verts_device_cords = [self.camera.project_point(self.mesh.transform.apply_to_point(p)) for vert in self.mesh.triangles for p in vert]
            w_values           = [self.camera.helper_w(self.mesh.transform.apply_to_point(p)) for vert in self.mesh.triangles for p in vert]

            verts_normals = []

            # applies the apply to normal from the transform to each vertex normal
            # QUESTION, is this correct way to do this?
            for vert in self.mesh.triangles:
                for p in vert:
                    index = (self.mesh.verts == p).all(axis=1).nonzero()
                    verts_index = index[0][0]
                    normal = self.mesh.vertex_normals[verts_index]
                    uv = self.mesh.uvs[verts_index]
                    verts_normals.append(Vector(self.mesh.transform.apply_to_normal(normal.to_array())))
                    uvs.append(uv)

            # Builds our screen transform matrix
            screen_cord_transform = np.array(([self.screen.width / 2, 0, self.screen.width / 2],
                                              [0, self.screen.height / 2, self.screen.height / 2],
                                              [0, 0, 1]))
            screen_cords = []
            depth = []
            # Applies our screen transform matrix
            for points in verts_device_cords:
                # takes off our depth values
                depth.append(points[2])
                # creates a modified array without the depth
                mod_points = np.array((points[0], points[1], 1))
                # applies our screen transform matrix to these new points
                screen_cords.append((np.matmul(screen_cord_transform, mod_points)))

                # converts the latest screen cords into ints
                screen_cords[-1] = np.array((int(screen_cords[-1][0]), int(screen_cords[-1][1]), 1))

            # for every 3 vertices in the triangle, we need to render the triangle
            num_triangles = len(self.mesh.triangles)

            for tri in range (0, num_triangles):
                # gives us the three vertices of the current triangle
                vertex_1 = screen_cords[3 * tri + 0]
                vertex_2 = screen_cords[3 * tri + 1]
                vertex_3 = screen_cords[3 * tri + 2]

                # gets our three depth values of the current triangle
                depth_1  = depth[3 * tri + 0]
                depth_2  = depth[3 * tri + 1]
                depth_3  = depth[3 * tri + 2]

                # normals are in the same order as the triangles. This should be same order as screen cords
                # This first gets our normal vector (that is normalized) and then applies the rotation to it using apply_to_normal
                normal = Vector(self.mesh.transform.apply_to_normal(self.mesh.normals[tri].to_array()))

                # may need to edit
                #vertex_normal = Vector(self.mesh.transform.apply_to_normal(self.mesh.vertex_normals[tri].to_array()))

                # check to see if we cull the normal. If returns True, we keep this triangle
                culling = self.cull(normal, cam)

                if culling == True:
                    # call screen.draw_triangle while passing it the three vertices of our triangle
                    x_y_list, bary_list = self.screen.draw_triangle(vertex_1, vertex_2, vertex_3)

                    # Now we have a list of every pixel for this triangle and what we need to render for it
                    for points in range (0, len(x_y_list)):
                        x, y = x_y_list[points]
                        alpha, beta, gamma = bary_list[points]

                        #depth checker
                        out_of_depth = False

                        # checks to see if triangle area is zero. If it is not, we need to render triangle
                        if alpha != -1 and beta != -1 and gamma != -1:

                            # Get our depth value by interpolation
                            z = depth_1 * alpha + depth_2 * beta + depth_3 * gamma

                            if shading == "depth":
                                z_depth = (z + 1) / 2

                                # checks to see if z out of range
                                if z_depth < 0 or z_depth > 1:
                                    out_of_depth = True

                                if z_depth > self.z_buffer[x, y] and out_of_depth == False:
                                    self.z_buffer[x, y] = z_depth
                                    image_buffer[x, y] = image_buffer[x, y] = (255 * z_depth, 255 * z_depth, 255 * z_depth)

                            else:
                                # checks to see if z out of range
                                if z < -1 or z > 1:
                                    out_of_depth = True

                                # checks our z_buffer for that current point to see if it needs to be overlapped
                                if z > self.z_buffer[x, y] and out_of_depth == False:

                                    # update our z_buffer!! (wow I am stupid)
                                    self.z_buffer[x, y] = z

                                    if shading == "flat":

                                        vertex_1 = Vector(verts_device_cords[3 * tri + 0]).to_array()
                                        vertex_2 = Vector(verts_device_cords[3 * tri + 1]).to_array()
                                        vertex_3 = Vector(verts_device_cords[3 * tri + 2]).to_array()

                                        # Gives us the top of I_d using light intensity and rgb value
                                        top_I_d = self.light.rgb * self.light.intensity

                                        # Gives us our p_world using vertex interlopation
                                        p_ndc = alpha * vertex_1 + beta * vertex_2 + gamma * vertex_3
                                        p_world = self.camera.inverse_project_point(p_ndc)
                                        p_world = Vector(p_world)

                                        # Gives us part of the I_d using vector subtraction
                                        bottom_I_d_partial = (Vector(self.light.transform.position) - p_world)

                                        # Gives full I_d by getting the magnitude and then squaring it
                                        bottom_I_d = bottom_I_d_partial.magnitude()**2

                                        # Gives us i_d by divison
                                        i_d = top_I_d/bottom_I_d

                                        # normalizes the light position, dots it with our normal, and then multiplies by kd/pi to give us the int part of phi_d
                                        int_phi_d = (self.mesh.kd/math.pi) * max(0, (bottom_I_d_partial.normalize().dot(normal)))

                                        # Gives us our total phi_d by multyping the int by each diffuse color part
                                        total_phi_d = (self.mesh.diffuse_color[0] * int_phi_d, self.mesh.diffuse_color[1] * int_phi_d, self.mesh.diffuse_color[2] * int_phi_d)

                                        # Gives us phi_d by taking the min in case greater than 1
                                        phi_d = (min(1, total_phi_d[0]), min(1, total_phi_d[1]), min(1, total_phi_d[2]))

                                        # gets our diffuse lighting
                                        diffuse_lighting = i_d * phi_d

                                        # gets final ambient lighting
                                        ambient_light_final = (ambient_light[0] * self.mesh.ka, ambient_light[1] * self.mesh.ka, ambient_light[2] * self.mesh.ka)

                                        # Gets total final light
                                        light_final = diffuse_lighting  + ambient_light_final
                                        # Adds color to image buffer
                                        image_buffer[x, y] = (int(light_final[0] * 255), int(light_final[1] * 255), int(light_final[2] * 255))

                                    # if our shading is barycentric, interolapte between RGB depending on bary cords
                                    if shading == "barycentric":
                                        image_buffer[x, y] = (255 * alpha, 255 * beta, 255 * gamma)

                                    if shading == "phong-blinn":
                                        vertex_1 = Vector(verts_device_cords[3 * tri + 0]).to_array()
                                        vertex_2 = Vector(verts_device_cords[3 * tri + 1]).to_array()
                                        vertex_3 = Vector(verts_device_cords[3 * tri + 2]).to_array()

                                        vertex_normal_1 = verts_normals[3 * tri + 0]
                                        vertex_normal_2 = verts_normals[3 * tri + 1]
                                        vertex_normal_3 = verts_normals[3 * tri + 2]

                                        # QUESTION is this the right way to get normal
                                        normal = vertex_normal_1.scalar_mul(alpha) + vertex_normal_2.scalar_mul(beta) + vertex_normal_3.scalar_mul(gamma)
                                        normal.normalize()

                                        # Gives us the top of I_d using light intensity and rgb value
                                        top_I_d = self.light.rgb * self.light.intensity

                                        # Gives us our p_world using vertex interlopation
                                        p_ndc = alpha * vertex_1 + beta * vertex_2 + gamma * vertex_3

                                        # QUESTION: How are we only doing one H solve? We have to get p_world every time...?
                                        # Or are we just doing L = self.light.transform.position and not caring about p_world?
                                        p_world = self.camera.inverse_project_point(p_ndc)
                                        p_world = Vector(p_world)

                                        # WRONG WRONG WRONG (was normalizing here)
                                        L = Vector(self.light.transform.position) - p_world

                                        V = (cam_world - p_world).normalize()



                                        # Gives us part of the I_d using vector subtraction
                                        bottom_I_d_partial = L

                                        # Gives full I_d by getting the magnitude and then squaring it
                                        bottom_I_d = bottom_I_d_partial.magnitude() ** 2
                                        L.normalize()
                                        H = (L + V).normalize()

                                        # Gives us i_d by divison
                                        i_d = top_I_d / bottom_I_d

                                        # normalizes the light position, dots it with our normal, and then multiplies by kd/pi to give us the int part of phi_d
                                        int_phi_d = (self.mesh.kd / math.pi) * max(0, (bottom_I_d_partial.normalize().dot(normal)))

                                        # Gives us our total phi_d by multyping the int by each diffuse color part
                                        total_phi_d = (self.mesh.diffuse_color[0] * int_phi_d, self.mesh.diffuse_color[1] * int_phi_d, self.mesh.diffuse_color[2] * int_phi_d)

                                        # Gives us phi_d by taking the min in case greater than 1
                                        phi_d = (min(1, total_phi_d[0]), min(1, total_phi_d[1]), min(1, total_phi_d[2]))

                                        # gets our diffuse lighting
                                        diffuse_lighting = i_d * phi_d

                                        # ADD specular lighting here
                                        # QUESTION getting around .06 for specular values? is that right?

                                        specular_light = self.mesh.specular_color * (self.mesh.ks * ((max(0, H.dot(normal)))**self.mesh.ke))

                                        # gets final ambient lighting
                                        ambient_light_final = (ambient_light[0] * self.mesh.ka, ambient_light[1] * self.mesh.ka, ambient_light[2] * self.mesh.ka)

                                        # Gets total final light
                                        light_final = diffuse_lighting + ambient_light_final + specular_light

                                        # Adds color to image buffer
                                        image_buffer[x, y] = (int(light_final[0] * 255), int(light_final[1] * 255), int(light_final[2] * 255))


                                    if shading == "texture":
                                        # take the uvs, then scale by
                                        # basically interlope, multiply by w and h, get closest int and then do
                                        # self.texture, what is closest pixel in image
                                        uv_1 = uvs[3 * tri + 0]
                                        uv_2 = uvs[3 * tri + 1]
                                        uv_3 = uvs[3 * tri + 2]

                                        uv = uv_1 * alpha + uv_2 * beta + uv_3 * gamma
                                        width = self.mesh.texture.shape[0] - 1
                                        height = self.mesh.texture.shape[1] - 1
                                        uv = np.array((int(uv[1] * width), int(uv[0] * height)))
                                        uv[0] = width - uv[0] - 1
                                        image_buffer[x, y] = self.mesh.texture[uv[0], uv[1]]


                                    if shading == "texture-correct":
                                        #undo the w divide, compute, u/w, etc and then interolpate using these
                                        #find w in inverse project point

                                        uv_1 = uvs[3 * tri + 0]
                                        uv_2 = uvs[3 * tri + 1]
                                        uv_3 = uvs[3 * tri + 2]

                                        w_1 = w_values[3 * tri + 0]
                                        w_2 = w_values[3 * tri + 1]
                                        w_3 = w_values[3 * tri + 2]

                                        uv_1 = uv_1 / w_1
                                        uv_2 = uv_2 / w_2
                                        uv_3 = uv_3 / w_3

                                        # so to get w, we have to

                                        new_depth = (1/w_1) * alpha + (1/w_2) * beta + (1/w_3) * gamma

                                        uv = uv_1 * alpha + uv_2 * beta + uv_3 * gamma

                                        uv = uv / new_depth

                                        height = self.mesh.texture.shape[0] - 1
                                        width  = self.mesh.texture.shape[1] - 1

                                        uv[0] = 1 - uv[0]

                                        if uv[1] < 0:
                                            uv[1] = 0
                                        if uv[1] > 1:
                                            uv[1] = 1
                                        if uv[0] < 0:
                                            uv[0] = 0
                                        if uv[0] > 1:
                                            uv[0] = 1
                                        uv = np.array((int(uv[1] * width), int(uv[0] * height)))
                                        image_buffer[x, y] = self.mesh.texture[uv[0], uv[1]]
        # renders our image buffer after all objects accounted for
        self.screen.draw(image_buffer)

    # takes in our normal vector and our camera vector and see if the point should be culled
    def cull(self, normal, cam):
        # returns the dot product of two vectors
        dot_product = cam.dot(normal)

        # if the dot product is greater than 0 then the vector is facing the camera and we don't need to worry about it
        if dot_product >= 0:
            return True
        return False
