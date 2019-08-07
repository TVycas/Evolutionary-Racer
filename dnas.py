# A class to describe a pseudo-DNA, i.e. genotype
#   Here, a virtual organism's DNA is an array of character.
#   Functionality:
#      -- convert DNA into a string
#      -- calculate DNA's "fitness"
#      -- mate DNA with another set of DNA
#      -- mutate DNA
import math
import map_handler
import logging
from p5 import *
from random import randrange, choice
from shapely.geometry import Point
from file_reader import read_track_files

logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO)


class DNA:

    # makes a random DNA
    def __init__(self, num, genes=None, id=-1):
        self.fitness = 0
        # TODO I can crate them or send them over
        self.polys = map_handler.create_checkpoint_polys(read_track_files(
            'track.txt'))
        self.path_list = []
        self.farthest_poly_reached = 0
        self.id = id

        # Add enough empty lists to the path_list so that the vectors in genes could be
        # devided to seperate to each polygon
        for i in range(0, len(self.polys)):
            self.path_list.append([])

        if genes is None:
            # The genetic sequence
            self.genes = []
            for x in range(0, int(num)):
                vec = Vector.random_2D()
                # TODO these should be variables
                vec.limit(5000, 3000)
                self.genes.append(vec)    # Pick from range of forces
        else:
            self.genes = genes

    def get_genes(self):
        return self.genes

    @staticmethod
    def vector_from_two_points(point1, point2):
        x = point2[0] - point1[0]
        y = point2[1] - point1[1]
        return Vector(x, y)

    # |AC x AB| / |AB| where AB is the line and C is the point
    def find_dist_to_next_poly(self, pos, current_polygon):
        current_poly_coords = list(current_polygon.exterior.coords)
        if len(current_poly_coords) > 3:
            ab = DNA.vector_from_two_points(current_poly_coords[2], current_poly_coords[3])

            ac = DNA.vector_from_two_points(current_poly_coords[2], pos)

            ac_ab_cross = ac.cross(ab)

            mag_of_ac_ab_cross = ac_ab_cross.magnitude
            mag_of_ab = ab.magnitude

            distance = mag_of_ac_ab_cross / mag_of_ab

            return distance
        else:
            return 0

    def find_current_polygon(self, pos):
        position = Point(pos)

        current_polygon = -1
        for i, poly in enumerate(self.polys):
            if poly.contains(position):
                current_polygon = i

        return current_polygon

    def calculate_fitness(self, pos):
        self.fitness = self.find_current_polygon(pos)

        if self.fitness != -1:
            dist_to_next_chpt = self.find_dist_to_next_poly(
                pos, self.polys[self.fitness])
            # TODO not sure how to remap this
            self.fitness += 1 - remap(dist_to_next_chpt, (0, 500), (0, 1))
            self.fitness *= self.fitness * self.fitness

        logging.debug("fitness = " + str(self.fitness))

    def add_to_path_list(self, pos, current_vector):
        current_pos = self.find_current_polygon(pos)

        if self.farthest_poly_reached <= current_pos:
            self.farthest_poly_reached = current_pos
            self.path_list[current_pos].append(current_vector)
        # If the car turns around we don't want to save that
        elif self.farthest_poly_reached > current_pos:
            return

    def remove_from_path_list(self, num_vec_to_remove):
        for i in range(num_vec_to_remove):
            if(len(self.path_list[self.farthest_poly_reached]) != 0):
                self.path_list[self.farthest_poly_reached].pop()
            else:
                break

    # Crossover
    def crossover(self, partner, mutation_rate):
        new_genes = []

        logging.info("\nMy id = " + str(self.id) + " my partner's id = " + str(partner.id))

        if logging.getLogger().getEffectiveLevel() == "DEBUG":
            logging.debug("\nmy_path_list - " + str(self.id) + "\n")
            for i, lst in enumerate(self.path_list):
                logging.debug("#" + str(i))
                for gene in lst:
                    logging.debug(gene)

            logging.debug("\npartner_path_list - " + str(partner.id) + "\n")
            for i, lst in enumerate(partner.path_list):
                logging.debugint("#" + str(i))
                for gene in lst:
                    logging.debug(gene)

            logging.debug("\nboth genes \n")
        for i, gene in enumerate(self.genes):
            logging.debug(str(gene) + " - " + str(partner.genes[i]))

        for i, gene_block in enumerate(self.path_list):
            if len(partner.path_list[i]) == 0 and len(gene_block) == 0:
                break

            new_genes.extend(choice([gene_block, partner.path_list[i]]))

            if new_genes == gene_block:
                logging.info("chosen block from id = " + str(self.id))
            else:
                logging.info("chosen block from id = " + str(partner.id))

        self.mutate(new_genes, mutation_rate)

        # Pad the rest of the genes with random vectors
        while len(new_genes) < len(self.genes):
            logging.debug("adds random vector")
            vec = Vector.random_2D()
            vec.limit(5000, 3000)
            new_genes.append(vec)

        while len(new_genes) > len(self.genes):
            logging.debug("removes vector")
            new_genes.pop()

        if logging.getLogger().getEffectiveLevel() == "DEBUG":
            logging.debug("\nnew_genes\n")
            for gene in new_genes:
                logging.debug(gene)


        return DNA(len(self.genes), new_genes)

    # Based on a mutation probability, picks a new random character
    def mutate(self, new_genes, mutation_rate):
        mutation_rate *= 100
        if randrange(0, 101) < mutation_rate:
            logging.info("mutated")
            # mutation only affects the end of the genes
            start_of_mutation = math.floor(len(self.genes) - (len(self.genes) * 0.2))
            for i in range(start_of_mutation, len(new_genes)):
                vec = Vector.random_2D()
                vec.limit(5000, 3000)
                new_genes[i] = vec

            return new_genes
