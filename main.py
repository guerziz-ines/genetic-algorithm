import sys
import operator
import os
import multiprocessing as mp
import numpy as np
from itertools import chain
import shape as Shape
import random
from copy import deepcopy
from population import Population
from PIL import Image

INITIAL_POPULATION = 20
GENETAIONS_PER_IMAGE = 50
ADD_PER_ITER = 10
MUTATION_CHANCE = 0.15
CROSSOVER_CHANCE = 0.6

try:
    global_target = Image.open("target.png")
except IOError:
    print("Can't found reference Image")
    exit()


def global_score(im1, im2):
    i1 = np.array(im1, np.int16)
    i2 = np.array(im2, np.int16)
    dif = np.sum(np.abs(i1 - i2))
    return (dif / 255.0 * 100) / i1.size


def mutateCrossOver(shapes):
    for s in shapes:
        case = np.random.random_sample()
        if case <= MUTATION_CHANCE:
            s.mutate()
        elif case <= CROSSOVER_CHANCE:
            s.crossover(random.choice(s.population.circles))
    return shapes


def create_nxt_generation(c, children_amount, p):
    results = p.map(mutateCrossOver, [c]*int(children_amount))
    result = list(chain(*results))

    return result

def run_ga(cores):
    if not os.path.exists("results"):
        os.mkdir("results")

    f = open(os.path.join("results", "log.txt"), 'a')
    target = global_target
    generation = 1
    parent = Population(target.size, INITIAL_POPULATION)

    prev_score = 101
    curr_img = parent.drawImage()
    score = global_score(curr_img, target)

    pp = mp.Pool(cores)

    while True:
            #print to console and log and save the picture every 50 iteration
            print("Generation: #{}, score: {}".format(generation, score))
            f.write("Generation: #{}, score: {}\n".format(generation, score))
            if generation % GENETAIONS_PER_IMAGE == 0:
                parent.drawImage().save(os.path.join("results", "{}.png".format(generation)))

            """score all shapes and sort them in by their fitness"""
            parent.scoreCircles(curr_img, target)
            parent.circles.sort(key=operator.attrgetter('fitness'))

            """take just the best 25%"""
            parent.circles = parent.circles[:round(len(parent.circles) * 0.25)]

            """start creating the next generation"""
            generation += 1
            children = deepcopy(parent)

            try:
                children.circles.extend(create_nxt_generation(children.circles, 5, pp))
            except KeyboardInterrupt:
                print("bye")
                pp.close()
                return

            parent = deepcopy(children)
            curr_img = parent.drawImage()
            score = global_score(curr_img, target)

if __name__ == "__main__":
    cores = max(1, mp.cpu_count()-1)

    run_ga(cores)