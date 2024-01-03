import numpy as np
import pygame
from vector import Vector

class Screen:

    def __init__(self, width, height):
        self.width  = width
        self.height = height

        pygame.init()

    def draw(self, image_buffer):
        # We test to make sure image_buffer is in correct format
        error_message = "Exception Raised: Numpy array is not a 3-D array in the format of (width, height, 3)"
        try:
            assert len(image_buffer)       == self.width
            assert len(image_buffer[0])    == self.height
            assert len(image_buffer[0][0]) == 3
        except ValueError as error_message:
            print(error_message)
        # Set our screen to be the size we are passed
        screen = pygame.display.set_mode((self.width, self.height))

        # We create a new surface that copies the numpy array of rgb values
        surface = pygame.pixelcopy.make_surface(image_buffer)

        # Flips image to see the default_output properly
        flipped_surface = pygame.transform.flip(surface, False, True)

        # This will draw our image onto the display, starting from destination 0,0

        screen.blit(flipped_surface, (0,0))
        pygame.display.update()

    # This handles case of multiple triangles so we can just update at the end and no rendering weirdness
    def draw_each_triangle(self, images):
        for image_buffer in images:
            self.draw(image_buffer)
        pygame.display.update()

    def show(self):
        # While this is false we will keep displaying the screen
        gameExit = False

        # This will actually do the displaying
        # While we are in this loop we will display the surface and keep updating the display
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
        # quit from pygame & python
        pygame.quit()
        quit()

    def ratio(self):
        return self.width/self.height

    def device_to_screen(self,p):
        pass

    def draw_triangle(self, endpoint_1, endpoint_2, endpoint_3):

        # Builds the rectangle of possible points for the triangle
        left_edge = min(endpoint_3[0], endpoint_2[0], endpoint_1[0])
        right_edge = max(endpoint_3[0], endpoint_2[0], endpoint_1[0])
        top_edge = min(endpoint_3[1], endpoint_2[1], endpoint_1[1])
        bottom_edge = max(endpoint_3[1], endpoint_2[1], endpoint_1[1])

        # For barycentric need triangle area
        triangle_area = self.cross_product(endpoint_1, endpoint_2, endpoint_3)

        # sets up some lists to return
        x_y_list = []
        bary_list = []
        # If using barycentric, each vertex has rgb value, then use barycentric values to multipy by point inside triangle

        """
                We will iterate through every pixel, if it does not fall inside the max rectangle formed by the triangular points
                we will ignore it and keep the color the same. Otherwise we run through the barycentric point check to see if the 
                point falls inside the triangle. If it does, we change the color.
                """

        for col in range(self.height):
            for row in range(self.width):
                # checks if pixel falls inside our rectangle
                if left_edge <= row <= right_edge and top_edge <= col <= bottom_edge:

                    # If pixel falls inside rectangle, see if it falls inside triangle by using barycentric
                    alpha, beta, gamma = self.barycentric((row, col), endpoint_1, endpoint_2, endpoint_3, triangle_area)

                    # If it does, we return our bary values and check them if falls inside triangle, add the row, col
                    # current endpoints and the bary cords for that triangle
                    if (0 <= alpha <= 1) and (0 <= beta <= 1) and (0 <= gamma <= 1):

                        x_y_list.append((row, col))
                        bary_list.append((alpha, beta, gamma))

        # return these values for that triangle
        return x_y_list, bary_list

    def cross_product(self, point_a, point_b, point_c):
        magnitude_cross_product = (point_b[1] - point_c[1]) * (point_a[0] - point_c[0]) + (point_c[0] - point_b[0]) * (
                    point_a[1] - point_c[1])

        return magnitude_cross_product

    def barycentric(self, point_p, point_a, point_b, point_c, triangle_area):
        alpha_top = (point_b[1] - point_c[1]) * (point_p[0] - point_c[0]) + (point_c[0] - point_b[0]) * (
                    point_p[1] - point_c[1])
        beta_top = (point_c[1] - point_a[1]) * (point_p[0] - point_c[0]) + (point_a[0] - point_c[0]) * (
                    point_p[1] - point_c[1])

        # if area equals zero, set all values to -1
        if triangle_area == 0.0:
            alpha = -1
            beta  = -1
            gamma = -1
        # else we calculate as normal
        else:
            alpha = alpha_top / triangle_area
            beta = beta_top / triangle_area
            gamma = 1 - alpha - beta
        # okay if bottom for triangle_area is zero skip
        '''if (alpha < 0) or (beta < 0) or (gamma < 0):
            return False
        return True'''
        # return these
        return alpha, beta, gamma


    