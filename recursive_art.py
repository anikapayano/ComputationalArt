""" Generate random art based on recursive functions.
    Additional functions are root and squared

    Building on for MP5, added Lamda functions and music visualizer

    Author: Anika Payano"""

import random
import math
from PIL import Image
import alsaaudio
import audioop
import pygame
import os

base1 = lambda x,y,t: x
base2 = lambda x,y,t: y
base3 = lambda x,y,t: t
prod = lambda x,y,t: x * y * t
avg = lambda x,y,t: (x+y+t)/3
cos_pi = lambda x,y,t: math.cos(math.pi* x)
sin_pi = lambda x,y,t: math.sin(math.pi* x)
squared = lambda x,y,t: x**2
root = lambda x,y,t: math.sqrt(abs(x))
functions = [base1, base2, base3, prod, avg, cos_pi, sin_pi, squared, root]



def build_random_function(depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth with lambda functions

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
    """
    if depth <= 1: #base case
        index = random.randint(0,2)
        return functions[index]
    else:
        index = random.randint(3,8)
        funct1 = build_random_function(depth-1)
        funct2 = build_random_function(depth-1)
        funct3 = build_random_function(depth-1)
        return lambda x, y, t: functions[index](funct1(x,y,t), funct2(x,y,t), funct3(x,y,t))


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    a = input_interval_end - input_interval_start
    b = output_interval_end - output_interval_start
    out = output_interval_start + (val - input_interval_start) * (b/a)
    return out

remap_interval(.5, 0, 1, 0, 10)


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350, t_size = 51):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    #red_function = ["x"]
    #green_function = ["y"]
    #blue_function = ["x"]
    depth = 7
    red_function = build_random_function(depth)
    green_function = build_random_function(depth)
    blue_function = build_random_function(depth)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for k in range(t_size):
        t = remap_interval(k, 0, t_size, -1, 1)
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(red_function(x, y, t)),
                        color_map(green_function(x, y, t)),
                        color_map(blue_function(x, y, t))
                        )

        im.save(filename + str(k) + ".png")
        print("Image " + str(k) + " created")

def imagelist(direc="Images"):
    """
    Converts all images in direc to pygame surfaces
    """ # List all files in directory
    files = [pygame.image.load("Images4" + os.sep + "img" + str(file_number) +
        ".png") for file_number in range(0,51)]  # Load the images using pygame
    return files


class Audio():

    def __init__(self):
        """
        Initializes a new Audio object.
        """
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, 0)
        self.inp.setchannels(1)
        self.inp.setrate(16000)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(160)

    def get_volume(self):
        """
        Returns the volume level at the current time.
        """
        l, data = self.inp.read()  # Read the input data
        if l:
            return audioop.rms(data, 2)  # Returns the current volume
        else:
            return 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()

#    generate_art("Images4/img")

    num_images = 50
    screen = pygame.display.set_mode((350, 350))
    audio = Audio()
    images = imagelist()
    running = True
    while running:
        level = int(audio.get_volume()/500)
        current = images[level % num_images]
        screen.blit(current, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # quits
                running = False
        pygame.display.flip()
