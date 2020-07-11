import logging
import pymunk
from cars import Car
from random import randrange

logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO, format='%(message)s')


class Population:

    def __init__(self, lifespan, map_handler, end_spread, mutations, pop_size):
        self.population = []            # Array to hold the current population
        self.mating_pool = []           # List which we will use for our "mating pool"
        self.generations = 0            # Number of generations
        self.finished = False           # Are we finished evolving?

        self.map_handler = map_handler
        self.mutation_rate = mutations        
        self.lifespan = lifespan
        self.end_spread = end_spread

        self.start_point = self.pick_start_point(self.map_handler.starting_line)

        # Creates the population of cars with random genes
        for id in range(0, pop_size):
            self.population.append(
                Car(self.map_handler, self.start_point, self.lifespan, self.end_spread, id))

    # Finds the midpoint of the line
    def pick_start_point(self, start_line):
        xs_avg = (start_line[0][0] + start_line[1][0]) / 2
        ys_avg = (start_line[0][1] + start_line[1][1]) / 2
        return (xs_avg, ys_avg)

    def calculate_fitness(self):
        for car in self.population:
            car.calculate_fitness()

    def natural_selection(self):
        # Clear the list
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
            
            # Create the mating pool where each car will get a number of slots corresponding their fitness
            for x in range(0, n):
                self.mating_pool.append(car.dna)

        logging.info("size of mating_pool = " + str(len(self.mating_pool)))

    # Create a new generation
    def generate(self):
        # Refill the population with children from the mating pool
        for i in range(len(self.population)):
            logging.debug("\nnew dna for car - " +
                          str(self.population[i].id) + "\n")

            # Pick two parents from the mating pool
            a = randrange(0, len(self.mating_pool))
            b = randrange(0, len(self.mating_pool))

            partnerA = self.mating_pool[a]
            partnerB = self.mating_pool[b]

            child = partnerA.crossover(partnerB, self.mutation_rate)

            # Create a new member of the population by overriding the old one
            self.population[i] = Car(self.map_handler, self.start_point, self.lifespan, self.end_spread, self.population[i].id, child)

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

        logging.info("best fitness - " + str(best_fitness))
        return pos

    # Updates and draws the cars
    def update_and_draw_cars(self):
        for car in self.population:
            # Updated the car with the next gene vector
            car.next_force()

            # Displays the car
            car.display()

            # Stops the simulation if a car has finished the track
            if not self.finished and car.finished:
                self.finished = True
                for body in self.map_handler.space.bodies:
                    if body.body_type == pymunk.Body.DYNAMIC:
                        self.map_handler.space.remove(body)
                break

        return self.finished
