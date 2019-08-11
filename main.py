import sys
import os
import multiprocessing as mp
import numpy as np
from copy import deepcopy
import shape as Shape
from population import Population
from PIL import Image

INITIAL_POPULATION = 20
GENETAIONS_PER_IMAGE = 50
ADD_PER_ITER = 10

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


def mutateCrossOver(population):
    c = deepcopy(population)
    c.mutate_or_crossOver()
    return c

def create_nxt_generation(pop, children_amount, p):
    results = p.map(mutateCrossOver, [pop]*int(children_amount))
    return results

def run_ga(cores):
    if not os.path.exists("results"):
        os.mkdir("results")

    f = open(os.path.join("results", "log.txt"), 'a')
    target = global_target
    generation = 1
    parent = Population(target.size, INITIAL_POPULATION)

    prev_score = 101
    score = global_score(parent.drawImage(), target)

    pp = mp.Pool(cores)

    while True:
            print("Generation: #{}, score: {}".format(generation, score))
            f.write("Generation: #{}, score: {}\n".format(generation, score))
            if generation % GENETAIONS_PER_IMAGE == 0:
                parent.drawImage().save(os.path.join("results", "{}.png".format(generation)))
            generation += 1
            prev_score = score
            children = []
            scores = []
            children.append(parent)
            scores.append(score)
            try:
                children.extend(create_nxt_generation(parent, ADD_PER_ITER, pp))
            except KeyboardInterrupt:
                print("bye")
                pp.close()
                return
            parent = children

if __name__ == "__main__":
    cores = max(1, mp.cpu_count()-1)

    run_ga(cores)