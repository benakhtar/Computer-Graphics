[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/TUFBi0xm)
# Programming Assignment 2

Class: CS 4204 (Computer Graphics), Fall 2023

Professor: Brendan David-John

## Overview

In this programming assignment, you are going to complete the second step towards building our renderer: the mesh module. As discussed in class, our renderer is going to be composed of several independent modules. The mesh module is responsible for definining mesh data as a collection of triangles represented via vertices and faces and for implementing relevant transformations in the rendering pipeline. Specifically, it will provide a class called `Mesh` that can load an stl file. An stl file for a simple unit cube consisting of 6 faces with 2 triangles each is provided. Please read the entire document before starting the assignment.


## Instructions

For this assignment, you will create a python file called `mesh.py`, and within that file there will be a class called `Mesh`. `Mesh` needs to be implemented as detailed below. Now that we know how to display a buffer of pixel values on the screen, we need to start implement the processing pipeline for 3D objects to eventually shade and display them. Specifically, you will implement a pipeline to read in an stl file (numpy-stl is reccomended) and generate lists of vertices, triangle faces, and normals. In this assignment we make use of printed numeric checks on known meshes to validate solutions, as true visual validation is not possible until we have methods to shade objects in our raster renderer.

*Hint*: this might be a good time to introduce a helper class for necessary mathematical structures such as 3D vectors.

### Output

The following should be the output when `assignment2.py` is run:

```bash
python assignment2.py
```

![default output](default_output.PNG)

The following should be the output when pytest with the verbose flag is run:

```bash
pytest -v assignment2.py
```

![test output](tests_output.PNG)

### Dependency Management
Each assignment will include a requirements.txt file that includes the python package requirements for the assignment. If you are using PyCharm it should automatically detect and install the dependencies when you create the virtual environment. Otherwise, [these instructions](https://www.jetbrains.com/help/pycharm/managing-dependencies.html#configure-requirements) will help you manually manage the requirements in PyCharm. If you are using something other than PyCharm, you can use the command line to manually install the packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```

Assignment 2 introduces a requirement for numpy-stl==3.0.1 

## The Mesh Class

### Exposed Members

#### `verts`
List of 3D vertices <x,y,z> for the mesh.

#### `faces`
List of triangle faces for the mesh, with each face defined as a list of 3 vertex indicies into `verts` in counter clockwise ordering.

#### `normals`
List of 3D face normals for the mesh. The elements of this list correspond to the same triangles defined in `faces`.

### Exposed Methods

#### `__init__(self)`
The constructor takes no required arguments.

#### `from_stl(stl_path)`
This static method takes an stl file as input, initializes an empty Mesh object and populates the `verts`, `faces`, `normals`, and `bounds` member variables. The method returns the populated Mesh object.

## Extra Credit
If you wish to receive the 1 extra credit point, you can create a program that uses the `Mesh` class to compute and print the spatial bounds in each dimension of an input stl file. This should be done in a separate file called `extracredit.py`. You must use the `Mesh` class and the methods you implemented earlier. When run with python, `extracredit.py` should print the minimum x, maximum x, minimum y, maximum y, minimum z, and maximum z of a specific stl file. The process to generate the stl file yourself is detailed below. This is something that you may want to implement in the future if you are interested in implementing spatial data structures such as a Boundary Volume Hierarchy.

Steps to generate an stl file for [Suzanne](https://www.dummies.com/article/technology/software/animation-software/blender/meet-suzanne-the-blender-monkey-142918/), Blender's iconic monkey face.
- Load a blank scene in Blender: Open Blender, create a new General file. Hit the delete key to delete the default cube in the scene. 
- Load the Suzanne mesh: Add an object to the scene (shift + a command) and select Mesh\Monkey.
- Export mesh as stl: Select File\Export\.stl. *important* be sure to check the Selection Only box on the right-side of the pop-up, listed under Include. Save this to your repo with a name like 'suzanne.stl'.

Using the Suzanne stl file print the bound values (be sure to print all three dimensions) with `extracredit.py`. The output will be compared to the correct values for the mesh to receive extra credit.

## Rubric
There are 10 points (11 with extra credit) for this assignment:
- *1 pts*: pytest test_from_stl passed without raising an exception
- *1 pts*: pytest test_list_sizes passed
- *4 pts*: Printed verts, faces, and normals values match expected output (see above)	
- *4 pts*: Printed verts, faces, and normals values match expected output for an stl file not provided as part of this repo
