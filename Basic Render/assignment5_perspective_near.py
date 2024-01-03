import numpy as np

from screen import Screen
from camera import PerspectiveCamera
from mesh import Mesh
from renderer import Renderer



if __name__ == '__main__':
    screen = Screen(500, 500)

    camera = PerspectiveCamera(0.75, -0.75, -0.75, 0.75, -0.5, -100)
    camera.transform.set_position(0, 5, 0)

    mesh = Mesh.from_stl("unit_cube.stl")
    mesh.transform.set_rotation(15, 0, 45)

    renderer = Renderer(screen, camera, mesh)
    renderer.render([50, 50, 100])

    screen.show()