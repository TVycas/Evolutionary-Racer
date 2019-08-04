import math
from p5 import *
from cars import Car
from random import randrange


class Population:

    def __init__(self, space, lifespan, start_line, target_line, mut, num):
        self.population = []            # Array to hold the current population
        self.mating_pool = []           # ArrayList which we will use for our "mating pool"
        self.generations = 0            # Number of generations
        self.finished = False           # Are we finished evolving?
        self.target_line = target_line  # Finish line
        self.mutation_rate = mut        # Mutation rate
        self.apply_force = True
        self.start_line = start_line
        self.start_point = self.pick_start_point(start_line)

        for id in range(0, num):
            self.population.append(
                Car(self.start_point, target_line, space, lifespan, id))

    # Finds the midpoint of the line
    def pick_start_point(self, start_line):
        xs_avg = (start_line[0][0] + start_line[1][0]) / 2
        ys_avg = (start_line[0][1] + start_line[1][1]) / 2
        return (xs_avg, ys_avg)

    def calculate_fitness(self):
        for car in self.population:
            car.calculate_fitness(self.start_line)

    def natural_selection(self):
        # Clear the ArrayList
        self.mating_pool = []
        max_fitness = 0
        for car in self.population:
            if car.dna.fitness > max_fitness:
                max_fitness = car.dna.fitness

        # Based on fitness, each member will get added to the mating pool a certain number of times
        # a higher fitness = more entries to mating pool = more likely to be picked as a parent
        # a lower fitness = fewer entries to mating pool = less likely to be picked as a parent
        for car in self.population:
            fitness = remap(car.dna.fitness, (0, max_fitness), (0, 1))
            # Arbitrary multiplier, we can also use monte carlo method
            n = math.floor(fitness * 100)
            print("\nFor car id - " + str(car.id) + ", with fitness " +
                  str(car.dna.fitness) + "we add " + str(n) + " dnas in the mating_pool\n")
            for x in range(0, n):               # and pick two random numbers
                self.mating_pool.append(car.dna)

        print("size of mating_pool = " + str(len(self.mating_pool)))

    # Create a new generation
    def generate(self):
        # Refill the population with children from the mating pool
        for car in self.population:
            print("\nnew dna for car - " + str(car.id) + "\n")
            a = randrange(0, len(self.mating_pool))
            b = randrange(0, len(self.mating_pool))
            print("a = " + str(a))
            print("b = " + str(b))

            partnerA = self.mating_pool[a]
            partnerB = self.mating_pool[b]

            child = partnerA.crossover(partnerB)

            child.mutate(self.mutation_rate)

            car.set_dna(child)
            car.reset_to_start()

        self.generations += 1
        print("\ngeneration #" + str(self.generations))

    # Compute the current "most fit" member of the population
    def evaluate(self):
        best = 0

        for car in self.population:
            if car.dna.fitness > best:
                best = car.dna.fitness

        print("\nbest fitness = " + str(best) + "\n")
        pos = (self.population[0].body.position.x, self.population[0].body.position.y)
        print("final location = " + str(pos))

    # Updates and draws the cars
    def draw_cars(self, mouse_x, mouse_y):
        for car in self.population:
            # TODO remove this check?
            # if self.apply_force:
            car.next_force()
            #   car.seek((mouse_x, mouse_y))
            car.display()
        # self.apply_force = False