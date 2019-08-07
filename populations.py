import math
import logging
from p5 import *
from cars import Car
from random import randrange

logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO)


class Population:

    def __init__(self, space, lifespan, checkpoint_polys, start_line, finish_line, mut, num):
        self.population = []            # Array to hold the current population
        self.mating_pool = []           # ArrayList which we will use for our "mating pool"
        self.generations = 0            # Number of generations
        self.finished = False           # Are we finished evolving?
        self.finish_line = finish_line  # Finish line
        self.mutation_rate = mut        # Mutation rate
        self.start_line = start_line
        self.start_point = self.pick_start_point(start_line)
        self.space = space
        self.lifespan = lifespan
        self.checkpoint_polys = checkpoint_polys

        for id in range(0, num):
            self.population.append(
                Car(self.checkpoint_polys, self.start_point, finish_line, space, self.lifespan, id))

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

        fitness_sum = 0
        max_fitness = 0
        for car in self.population:
            fitness_sum += car.dna.fitness
            if car.dna.fitness > max_fitness:
                max_fitness = car.dna.fitness

        fitness_sum = fitness_sum / 100

        for car in self.population:
            n = int(round(car.dna.fitness / fitness_sum))
            # Add weight to the best performing dna
            if car.dna.fitness == max_fitness:
                n += 25

            logging.info("\nFor car id - " + str(car.id) + ", with fitness " +
                         str(car.dna.fitness) + " we add " + str(n) + " dnas in the mating_pool")

            for x in range(0, n):
                self.mating_pool.append(car.dna)

        logging.info("size of mating_pool = " + str(len(self.mating_pool)))

    # Create a new generation
    def generate(self):
        # Refill the population with children from the mating pool
        for i in range(len(self.population)):
            logging.debug("\nnew dna for car - " + str(self.population[i].id) + "\n")
            a = randrange(0, len(self.mating_pool))
            b = randrange(0, len(self.mating_pool))

            partnerA = self.mating_pool[a]
            partnerB = self.mating_pool[b]

            child = partnerA.crossover(partnerB, self.mutation_rate)

            self.population[i] = Car(self.checkpoint_polys, self.start_point, self.finish_line,
                                     self.space, self.lifespan, self.population[i].id, child)

        self.generations += 1

        logging.info("\ngeneration #" + str(self.generations))

    # Compute the current "most fit" member of the population
    def evaluate(self):
        best_fitness = 0
        best_car = None

        for car in self.population:
            if car.dna.fitness > best_fitness:
                best_fitness = car.dna.fitness
                best_car = car

        pos = (best_car.body.position.x, best_car.body.position.y)
        logging.info("best fitness" + str(best_fitness))
        return pos

    # Updates and draws the cars
    def draw_cars(self, mouse_x, mouse_y):
        for car in self.population:
            car.next_force()
            # car.seek((mouse_x, mouse_y))
            car.display()
