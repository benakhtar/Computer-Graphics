import numpy as np

from screen import Screen
from mesh import Mesh
from transform import Transform
from camera import OrthoCamera
from vector import Vector

import numpy as np

def render_triangle():
    width = 500
    height = 500

    # define 3D triangle in world space
    triangle = Mesh()
    triangle.verts = [np.array([-0.5, -0.5, 0.25]), np.array([-1.0, -0.65, 0.5]), np.array([-0.75, -0.85, 0.65])]
    triangle.faces = [[2, 1, 0]]
    triangle.normals = [np.array([0, 1, 0])]

    # define an ortho camera
    camera = OrthoCamera(1.5, -1.5, -1.5, 1.5, -1, -50)
    camera.transform.set_position(-.5, 0, 0)

    # define a screen and background/foreground colors for silhouette
    bg_color  = (255, 255, 255)
    obj_color = (0, 0, 0)

    screen = Screen(width, height)
    image_buffer = np.full((height, width, 3), bg_color)

    verts_device_coords = [camera.project_point(triangle.transform.apply_to_point(p)) for p in triangle.verts]
    
    #TODO: transform verts_device_coords from device (normalized) to screen (pixel) coordinates

    # Builds our screen transform matrix
    screen_cord_transform = np.array(([width/2, 0, width/2],
                                      [0, height/2, height/2],
                                      [0, 0, 1]))
    screen_coords = []
    depths = []
    # Applies our screen transform matrix
    for points in verts_device_coords:
        depths.append(points[2])
        # Removes depth point
        mod_points = np.array((points[0], points[1], 1))
        screen_coords.append((np.matmul(screen_cord_transform, mod_points)))

    # Sets pixels to ints
    for x in range(0, len(screen_coords)):
        for y in range(0, len(screen_coords[0])):
            screen_coords[x][y] = int(screen_coords[x][y])
    #TODO: determine which pixels to check for rendering triangle (bounding box in screen coordinates)

    #TODO: loop over pixels, check which are inside the triangle and set image_buffer at that pixel = obj_color.

    # Builds our endpoints
    endpoint_1 = [screen_coords[0][0], screen_coords[0][1]]
    endpoint_2 = [screen_coords[1][0], screen_coords[1][1]]
    endpoint_3 = [screen_coords[2][0], screen_coords[2][1]]

    # Checks pixels
    image_buffer = screen.draw_triangle(obj_color, image_buffer, endpoint_1, endpoint_2, endpoint_3)

    # Draws our image
    screen.draw(image_buffer)

    screen.show()

if __name__ == '__main__':
    render_triangle()
    