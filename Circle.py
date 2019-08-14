import random

import numpy as np
from PIL import Image
from PIL import ImageDraw
from scipy.ndimage.filters import generic_filter as gf


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __str__(self):
        return "Point: [{}, {}]".format(self.x, self.y)

    def __repr__(self):
        return {'x':self.x, 'y':self.y}


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, c):
        self.r = max(0, min(255, self.r + c.r))
        self.g = max(0, min(255, self.g + c.g))
        self.b = max(0, min(255, self.b + c.b))

    def _shift(self, c):
        self.r = c.r
        self.g = c.g
        self.b = c.b

    def __str__(self):
        return "({}, {}, {})".format(self.r, self.g, self.b)

    def __repr__(self):
        return {'Color red': self.r, 'green': self.g, 'blue':self.b}


# Implementation of circle only.
class Circle:
    def __init__(self, imgSz, pop):
        self.pos = Point(random.randint(0, imgSz[0]), random.randint(0, imgSz[1]))
        self.diameter = random.randint(5, 15)
        self.imgSz = imgSz
        self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.params = ["diameter", "color", "pos"]
        self. fitness = -1
        self. population = pop

    #picking random parameter and changed it randomalic
    def mutate(self):
        mutant_param = random.choice(self.params)

        if mutant_param == 'diameter':
            self.diameter = random.randint(5, 15)
        elif mutant_param == 'color':
            self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.pos = Point(random.randint(0, self.imgSz[0]), random.randint(0, self.imgSz[1]))

    def crossover(self, parentB):
        #CrossOver formula: assuming we have 2 shapes taken posA, diameterB and mean(RGB)

        self.pos.x = np.mean((self.pos.x, parentB.pos.x)).astype('int16')
        self.pos.y = np.mean((self.pos.y, parentB.pos.y)).astype('int16')
        self.diameter = np.mean((self.diameter, parentB.diameter)).astype('int16')
        self.color = Color(np.mean((self.color.r, parentB.color.r), dtype=int),
                                np.mean((self.color.g, parentB.color.g), dtype=int),
                                np.mean((self.color.b, parentB.color.b), dtype=int))

    def save_shape(self):

        shape = {}
        shape["imgSz"] = self.imgSz
        shape["diameter"] = self.diameter
        shape["color"] = (self.color.r, self.color.g, self.color.b)
        shape["pos"] = (self.pos.x, self.pos.y)
        shape["fitness"] = self.fitness

        return shape

    def load_shape(self, ref_shape):
        self.imgSz = ref_shape["imgSz"]
        self.diameter = ref_shape.diameter
        self.pos = Point(ref_shape.pos.x, ref_shape.pos.y)
        self.color = Color(ref_shape.color.r, ref_shape.color.g, ref_shape.color.b)
        self.fitness = ref_shape.fitness

    def score(self, im_diff):
        a, b = self.pos.x, self.pos.y
        r = np.round(self.diameter / 2).astype('int')
        n = 2*r + 1
        data = im_diff[b-r:b+r+1, a-r:a+r+1, :]

        kernel = np.zeros((n, n, 3))
        y, x = np.ogrid[-r:r+1, -r:r+1]
        mask_circle = x**2 + y**2 <= r**2
        kernel[mask_circle] = 1
        #need to chek this line
        fitness = np.mean(np.mean(np.mean(gf(data, np.mean, footprint=kernel))))

        self.fitness = fitness

# functions for debugging the classes
def drawImage(shapes):
    image = Image.new('RGB', (250, 250), (255, 255, 255))
    example2paint = ImageDraw.Draw(image)

    for shapeIdx in shapes:
        h = (shapeIdx.color.r, shapeIdx.color.g, shapeIdx.color.b)
        example2paint.ellipse([shapeIdx.pos.y - shapeIdx.diameter, shapeIdx.pos.x - shapeIdx.diameter,
                               shapeIdx.pos.y + shapeIdx.diameter, shapeIdx.pos.x + shapeIdx.diameter], outline=h, fill=h)

    return image


def test_function():

    A = Shape((250, 250))
    B = Shape((250, 250))
    shapes = (A, B)
    img = drawImage(shapes)
    img.show(title= 'Orginal')
    A.mutate()
    B.mutate()

    img1 = drawImage(shapes)

    C = A.crossover(B)
    shapes = (A, B, C)
    img2 = drawImage(shapes=shapes)
    img2.show(title='After CrossOver')

    i1 = np.array(img1, np.int16)
    i2 = np.array(img2, np.int16)

    result = np.abs(i1 - i2).astype('uint8')

    im3 = Image.fromarray(result)

    im3.show()