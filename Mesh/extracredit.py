from mesh import Mesh

def min_max_dimensions():
    mesh = Mesh()
    mesh.from_stl("suzanne.stl")
    min_x = 0.0
    max_x = 0.0
    min_y = 0.0
    max_y = 0.0
    min_z = 0.0
    max_z = 0.0
    first_loop = True

    for coordinate in range(0, len(mesh.verts)):
        # Need to ensure that don't get stuck with initial values
        if first_loop:
            min_x = mesh.verts[coordinate][0]
            max_x = mesh.verts[coordinate][0]
            min_y = mesh.verts[coordinate][1]
            max_y = mesh.verts[coordinate][1]
            min_z = mesh.verts[coordinate][2]
            max_z = mesh.verts[coordinate][2]
        else:
            min_x = min(min_x, mesh.verts[coordinate][0])
            max_x = max(max_x, mesh.verts[coordinate][0])
            min_y = min(min_y, mesh.verts[coordinate][1])
            max_y = max(max_y, mesh.verts[coordinate][1])
            min_z = min(min_z, mesh.verts[coordinate][2])
            max_z = max(max_z, mesh.verts[coordinate][2])

        first_loop = False

    # How do you want us to print?
    # formatting for printing
    # mesh.bounds = ((min_x, max_x), (min_y, max_y), (min_z, max_z))

    print((min_x, max_x), (min_y, max_y), (min_z, max_z))


if __name__ == '__main__':
    min_max_dimensions()