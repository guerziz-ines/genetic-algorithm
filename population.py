import numpy as np
import matplotlib as plt
import random
from PIL import Image
from PIL import ImageDraw
from copy import deepcopy
import shape as Shape

MUTATION_CHANCE = 0.15


class Population:
    def __init__(self, imgSz, population_amount):
        self.imgSz = imgSz
        self.circles = [Shape(imgSz) for _ in range(population_amount)]

    def mutate(self):
        for s in random.sample(self.circles, int(len(self.circles) * MUTATION_CHANCE)):
            s.mutate()

    def drawImage(self):

        image = Image.new('RGB', (250, 250), (255, 255, 255))
        can = ImageDraw.Draw(image)

        for shapeIdx in self.circles:
            hue = (shapeIdx.color.r, shapeIdx.color.g, shapeIdx.color.b)
            can.ellipse([shapeIdx.pos.x - shapeIdx.diameter, shapeIdx.pos.y - shapeIdx.diameter,
                                   shapeIdx.pos.x + shapeIdx.diameter, shapeIdx.pos.y + shapeIdx.diameter], outline=hue,
                                  fill=hue)

        return image

