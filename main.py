import operator
import os
import multiprocessing as mp
from itertools import chain
from copy import deepcopy
from population import Population
from PIL import Image

INITIAL_POPULATION = 100
GENETAIONS_PER_IMAGE = 6
ADD_PER_ITER = 10
SAVED_POPULATION = 0.1


try:
    global_target = Image.open("target.png")
except IOError:
    print("Can't found reference Image")
    exit(1)


class GA:
    def __init__(self, target, cores):
        self.target = target
        self.cores = cores
        self.generation = 1
        self.parent = Population(target.size, INITIAL_POPULATION)
        self.curr_img = self.parent.drawImage()
        self.score = 100

    def run_GA(self):
        if not os.path.exists("results"):
            os.mkdir("results")

        f = open(os.path.join("results", "log.txt"), 'a')

        pp = mp.Pool(self.cores)

        while True:
        # print to console and log and save the picture every 50 iteration
            print("Generation: #{}, score: {}".format(self.generation, self.score))
            f.write("Generation: #{}, score: {}\n".format(self.generation, self.score))

            if self.generation % GENETAIONS_PER_IMAGE == 0:
                self.parent.drawImage().save(os.path.join("results", "{}.png".format(generation)))

            #score all shapes and sort them in by their fitness
            self.parent.scoreCircles(self.curr_img, self.target)
            self.parent.circles.sort(key=operator.attrgetter('fitness'))

            #take just the best 10%
            self.parent.circles = self.parent.circles[:round(len(self.parent.circles) * SAVED_POPULATION)]

            #start creating the next generation
            self.generation += 1
            children = deepcopy(self.parent)

            try:
                children.circles.extend(self.create_nxt_generation(children.circles, ADD_PER_ITER, pp))
            except KeyboardInterrupt:
                print("bye")
                pp.close()
                return

            self.curr_img = children.drawImage()
            self.score = children.global_score(self.curr_img, self.target)
            self.parent = deepcopy(children)

    def create_nxt_generation(self, c, children_amount, p):
        results = p.map(self.parent.mutateCrossOver, [c]*int(children_amount))
        result = list(chain(*results))

        return result


if __name__ == "__main__":
    cores = max(1, mp.cpu_count()-1)

    algo = GA(global_target, cores)
    algo.run_GA()