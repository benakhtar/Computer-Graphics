import numpy as np

from screen import Screen
from camera import OrthoCamera
from mesh import Mesh
from renderer import Renderer



if __name__ == '__main__':
    screen = Screen(500, 500)

    camera = OrthoCamera(0.75, -0.75, -0.75, 0.75, -0.5, -100)
    camera.transform.set_position(0, 15, 0)

    mesh = Mesh.from_stl("unit_cube.stl")
    mesh.transform.set_rotation(15, 0, 45)

    renderer = Renderer(screen, camera, mesh)
    renderer.render([100, 50, 50])

    screen.show()