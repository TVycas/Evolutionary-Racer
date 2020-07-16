import pymunk
from cars import Car
from random import randrange


class Population:

    def __init__(self, num_of_genes, map_handler, end_spread, mutation_rate, pop_size):
        """Sets up the object and creates the initial population of Car objects.

        Args:
            num_of_genes (int): The number of genes per car.
            map_handler (MapHandler obj): An object for controlling the map.
            end_spread (int): The number of genes to remove and replace from the end of the gene list.
            mutation_rate (float): The chance of the Dna to mutate.
            pop_size (int): The number of Cars in the population.
        """
        self.population = []            # Array to hold the current population
        self.mating_pool = []           # List which we will use for our "mating pool"
        self.generations = 0            # Number of generations
        self.finished = False           # Are we finished evolving?

        self.map_handler = map_handler
        self.mutation_rate = mutation_rate
        self.num_of_genes = num_of_genes
        self.end_spread = end_spread

        self.start_point = map_handler.find_line_midpoint(self.map_handler.starting_line)

        # Creates the population of cars with random genes
        for id in range(0, pop_size):
            self.population.append(
                Car(self.map_handler, self.start_point, self.num_of_genes, self.end_spread, id))

    def calculate_fitness(self):
        """Calculates the fitness of each Car in the population."""
        for car in self.population:
            car.calculate_fitness()

    def fitness_proportionate_selection(self):
        """Fitness proportionate selection done over the entire population.
        Creates a "mating pool" where the higher the fitness value of the Car, the
        more entries in the pool it gets. This way, it gets better chances to get
        picked when constructing new generation.
        """

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

            # Create the mating pool where each car will get a number of entries corresponding their fitness
            for x in range(0, n):
                self.mating_pool.append(car.dna)

    def crossover(self):
        """Constructs a new generation using the mating pool."""

        # Refill the population with children from the mating pool
        for i in range(len(self.population)):
            # Pick two parents from the mating pool
            a = randrange(0, len(self.mating_pool))
            b = randrange(0, len(self.mating_pool))

            partnerA = self.mating_pool[a]
            partnerB = self.mating_pool[b]

            child = partnerA.crossover(partnerB, self.mutation_rate)

            # Create a new member of the population by overriding the old one
            self.population[i] = \
                Car(self.map_handler, self.start_point, self.num_of_genes,
                    self.end_spread, self.population[i].id, child)

        self.generations += 1

    def evaluate(self):
        """Computes the current "most fit" member of the population.

        Returns:
            [tuple]: The position of the most fit member of the population.
        """
        best_fitness = 0
        best_car = None

        for car in self.population:
            if car.dna.fitness > best_fitness:
                best_fitness = car.dna.fitness
                best_car = car

        pos = (best_car.body.position.x, best_car.body.position.y)

        return pos

    def move_and_draw_cars(self):
        """Moves and draws each of the Cars in the population.

        Returns:
            bool: Returns True if any of the cars finished.
        """
        for car in self.population:
            # Updated the car with the next gene vector
            car.next_force()

            # Displays the car
            car.display()

            # Stops the simulation if a car has finished the track
            if not self.finished and car.finished:
                self.finished = True
                self._stop_simulation()
                break

        return self.finished

    def _stop_simulation(self):
        for body in self.map_handler.space.bodies:
            if body.body_type == pymunk.Body.DYNAMIC:
                self.map_handler.space.remove(body)
