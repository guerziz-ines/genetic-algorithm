import numpy as np
import random
from PIL import Image
from PIL import ImageDraw
from Circle import Circle

#params
MUTATION_CHANCE = 0.15
CROSSOVER_CHANCE = 0.6


""" Population class managing all the shapes in our picture
    data fields: 
    imgSz - target img size width*heighet
    circles - all the circles in our image"""


class Population:
    def __init__(self, imgSz, population_amount):
        self.imgSz = imgSz
        self.circles = [Circle(imgSz, self) for _ in range(population_amount)]


    def scoreCircles(self, im1, im2):
        i1 = np.array(im1, np.int16)
        i2 = np.array(im2, np.int16)
        dif = np.abs(i1 - i2)
        for c in self.circles:
            c.score(dif)

    def drawImage(self):
        image = Image.new('RGB', self.imgSz, (255, 255, 255))
        canvas = ImageDraw.Draw(image)

        for shapeIdx in self.circles:
            hue = (shapeIdx.color.r, shapeIdx.color.g, shapeIdx.color.b)
            canvas.ellipse([shapeIdx.pos.x - shapeIdx.diameter, shapeIdx.pos.y - shapeIdx.diameter,
                                   shapeIdx.pos.x + shapeIdx.diameter, shapeIdx.pos.y + shapeIdx.diameter], outline=hue,
                                   fill=hue)
        return image

    def getSave(self, generation):
        so = [generation]
        return so + [c.getSave() for c in self.circles]

    def loadSave(self, so):
        self.circles = []
        gen = so[0]
        so = so[1:]
        for c in so:
            newGene = Population(self.imgSz)
            newGene.loadSave(c)
            self.circles.append(newGene)
        return gen

    def global_score(self, im1, im2):
        i1 = np.array(im1, np.int16)
        i2 = np.array(im2, np.int16)
        dif = np.sum(np.abs(i1 - i2))
        return (dif / 255.0 * 100) / i1.size

    def mutateCrossOver(self, shapes):
        for s in shapes:
            case = np.random.random_sample()
            if case <= MUTATION_CHANCE:
                s.mutate()
            elif case <= CROSSOVER_CHANCE:
                s.crossover(random.choice(s.population.circles))
        return shapes
