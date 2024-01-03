from screen import Screen
from camera import PerspectiveCamera
from mesh import Mesh
import numpy as np


class Renderer:

    def __init__(self, screen, camera, mesh):
        self.screen = screen
        self.camera = camera
        self.mesh   = mesh

    def render(self, bg_color):
        # define a screen and background/foreground colors for silhouette
        bg_color = bg_color
        obj_color = (0, 0, 0)

        image_buffer = np.full((self.screen.height, self.screen.width, 3), bg_color)

        # Need to get every vert
        verts_device_cords = [self.camera.project_point(self.mesh.transform.apply_to_point(p)) for vert in self.mesh.triangles for p in vert]

        # Builds our screen transform matrix
        screen_cord_transform = np.array(([self.screen.width / 2, 0, self.screen.width / 2],
                                          [0, self.screen.height / 2, self.screen.height / 2],
                                          [0, 0, 1]))
        screen_cords = []
        depths = []

        # Applies our screen transform matrix
        for points in verts_device_cords:
            depths.append(points[2])
            # Removes depth point
            mod_points = np.array((points[0], points[1], 1))
            screen_cords.append((np.matmul(screen_cord_transform, mod_points)))

        # Sets pixels to ints
        for x in range(0, len(screen_cords)):
            for y in range(0, len(screen_cords[0])):
                screen_cords[x][y] = int(screen_cords[x][y])

        # Builds our endpoints
        images = []
        for tri in range(0, int(len(screen_cords)/3)):
            endpoint_1 = [screen_cords[3 * tri + 0][0], screen_cords[3 * tri + 0][1]]
            endpoint_2 = [screen_cords[3 * tri + 1][0], screen_cords[3 * tri + 1][1]]
            endpoint_3 = [screen_cords[3 * tri + 2][0], screen_cords[3 * tri + 2][1]]
            # Checks pixels
            images.append(self.screen.draw_triangle(obj_color, image_buffer, endpoint_1, endpoint_2, endpoint_3))

        # Draws our image
        self.screen.draw_each_triangle(images)
