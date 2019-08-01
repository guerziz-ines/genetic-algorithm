import numpy as np
import matplotlib as plt
import random
from PIL import Image
from PIL import ImageDraw
from copy import deepcopy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)


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

# Implementation of circle only.
class Shape:
    def __init__(self, imgSz):
        self.pos = Point(random.randint(0, imgSz[0], random.randint(0, imgSz[1])))
        self.diameter = random.randint(5, 15)
        self.imgSz = imgSz
        self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.params = ["diameter", "color", "pos"]
        self. fitness = -1

    def mutate(self):




