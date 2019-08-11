import sys
import os
import numpy as np
import matplotlib as plt
import random
from PIL import Image
from PIL import ImageDraw
from shape import Shape
import multiprocessing as mp

MUTATION_CHANCE = 0.15
CROSSOVER_CHANCE = 0.35


class Population:
    def __init__(self, imgSz, population_amount):
        self.imgSz = imgSz
        self.circles = [Shape(imgSz) for _ in range(population_amount)]

    def mutate_or_crossOver(self):

        for s in random.sample(self.circles, int(len(self.circles) * MUTATION_CHANCE)):
            s.mutate()

        for s in random.sample(self.circles, int(len(self.circles) * CROSSOVER_CHANCE)):
                s.crossover(random.sample(self.circles, 1))

    def drawImage(self):

        image = Image.new('RGB', self.imgSz, (255, 255, 255))
        can = ImageDraw.Draw(image)

        for shapeIdx in self.circles:
            hue = (shapeIdx.color.r, shapeIdx.color.g, shapeIdx.color.b)
            can.ellipse([shapeIdx.pos.x - shapeIdx.diameter, shapeIdx.pos.y - shapeIdx.diameter,
                                   shapeIdx.pos.x + shapeIdx.diameter, shapeIdx.pos.y + shapeIdx.diameter], outline=hue,
                                   fill=hue)

        return image

    def getSave(self, generation):
        """
        Allows us to save an individual organism in case the program is stopped.
        """
        so = [generation]
        return so + [c.getSave() for c in self.circles]

    def loadSave(self, so):
        """
        Allows us to load an individual organism in case the program is stopped.
        """
        self.circles = []
        gen = so[0]
        so = so[1:]
        for c in so:
            newGene = Population(self.imgSz)
            newGene.loadSave(c)
            self.circles.append(newGene)
        return gen


