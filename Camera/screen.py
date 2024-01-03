import pygame

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

        # This will draw our checkboard onto the display, starting from destination 0,0

        screen.blit(flipped_surface, (0,0))

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

    def draw_triangle(self, obj_color, image_buffer, endpoint_1, endpoint_2, endpoint_3):
        left_edge = min(endpoint_3[0], endpoint_2[0], endpoint_1[0])
        right_edge = max(endpoint_3[0], endpoint_2[0], endpoint_1[0])
        top_edge = min(endpoint_3[1], endpoint_2[1], endpoint_1[1])
        bottom_edge = max(endpoint_3[1], endpoint_2[1], endpoint_1[1])

        # For barycentric need triangle area
        triangle_area = self.cross_product(endpoint_1, endpoint_2, endpoint_3)

        """
        We will iterate through every pixel, if it does not fall inside the max rectangle formed by the triangular points
        we will ignore it and keep the color the same. Otherwise we run through the barycentric point check to see if the 
        point falls inside the triangle. If it does, we change the color.
        """
        for col in range(self.height):
            for row in range(self.width):
                if left_edge <= row <= right_edge and top_edge <= col <= bottom_edge:
                    if self.barycentric_check((row, col), endpoint_1, endpoint_2, endpoint_3, triangle_area):
                        #color = obj_color
                        image_buffer[row, col] = obj_color

        return image_buffer

    def cross_product(self, point_a, point_b, point_c):
        magnitude_cross_product = (point_b[1] - point_c[1]) * (point_a[0] - point_c[0]) + (point_c[0] - point_b[0]) * (
                    point_a[1] - point_c[1])

        return magnitude_cross_product

    def barycentric_check(self, point_p, point_a, point_b, point_c, triangle_area):
        alpha_top = (point_b[1] - point_c[1]) * (point_p[0] - point_c[0]) + (point_c[0] - point_b[0]) * (
                    point_p[1] - point_c[1])
        beta_top = (point_c[1] - point_a[1]) * (point_p[0] - point_c[0]) + (point_a[0] - point_c[0]) * (
                    point_p[1] - point_c[1])

        alpha = alpha_top / triangle_area
        beta = beta_top / triangle_area
        gamma = 1 - alpha - beta

        if (alpha < 0) or (beta < 0) or (gamma < 0):
            return False
        return True


    