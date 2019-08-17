# A class to describe a pseudo-DNA, i.e. genotype
#   Here, a virtual organism's DNA is an array of character.
#   Functionality:
#      -- convert DNA into a string
#      -- calculate DNA's "fitness"
#      -- mate DNA with another set of DNA
#      -- mutate DNA
import logging
import math
from p5 import *
from random import randrange, choice
from shapely.geometry import Point

logging.basicConfig(filename='log.txt', filemode='w',
                    level=logging.INFO, format='%(message)s')


class DNA:

    def __init__(self, checkpoint_polys, num, genes=None, mutated=False, id=-1):
        self.fitness = 0
        self.polys = checkpoint_polys
        self.path_list = []
        self.farthest_poly_reached = 0
        self.id = id
        self.num_of_genes = num
        self.mutated = mutated

        self.max_checkpnt_len = width if width > height else height

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

    def get_next_gene(self):
        if len(self.genes) > 0:
            return self.genes.pop(0)
        else:
            return None

    @staticmethod
    def vector_from_two_points(point1, point2):
        x = point2[0] - point1[0]
        y = point2[1] - point1[1]
        return Vector(x, y)

    # |AC x AB| / |AB| where AB is the line and C is the point
    def find_dist_to_next_poly(self, pos, current_polygon):
        current_poly_coords = list(current_polygon.exterior.coords)
        if len(current_poly_coords) > 3:
            ab = DNA.vector_from_two_points(
                current_poly_coords[2], current_poly_coords[3])

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

            self.fitness += 1 - remap(dist_to_next_chpt, (0, self.max_checkpnt_len), (0, 1))
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
        pb_to_remove_from = self.farthest_poly_reached
        for i in range(num_vec_to_remove):
            if(len(self.path_list[pb_to_remove_from]) != 0):
                self.path_list[pb_to_remove_from].pop()
            elif (pb_to_remove_from - 1) >= 0:
                pb_to_remove_from -= 1
            else:
                break

    def crossover(self, partner, mutation_rate):
        new_genes = []

        logging.info("\nMy id = " + str(self.id) +
                     " my partner's id = " + str(partner.id))

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            logging.debug("\nmy_path_list - " + str(self.id) + "\n")
            for i, lst in enumerate(self.path_list):
                logging.debug("#" + str(i))
                for gene in lst:
                    logging.debug(gene)

            logging.debug("\npartner_path_list - " + str(partner.id) + "\n")
            for i, lst in enumerate(partner.path_list):
                logging.debug("#" + str(i))
                for gene in lst:
                    logging.debug(gene)

        for i, gene_block in enumerate(self.path_list):
            if len(partner.path_list[i]) == 0 and len(gene_block) == 0:
                break

            new_genes.extend(choice([gene_block, partner.path_list[i]]))

            if new_genes == gene_block:
                logging.info("chosen block from id = " + str(self.id))
            else:
                logging.info("chosen block from id = " + str(partner.id))

        mutated, new_genes = self.mutate(new_genes, mutation_rate)

        # Pad the rest of the genes with random vectors
        while len(new_genes) < self.num_of_genes:
            logging.debug("adds random vector")
            vec = Vector.random_2D()
            vec.limit(5000, 3000)
            new_genes.append(vec)

        while len(new_genes) > self.num_of_genes:
            logging.debug("removes vector")
            new_genes.pop()

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            logging.debug("\nnew_genes\n")
            for gene in new_genes:
                logging.debug(gene)

        return DNA(self.polys, self.num_of_genes, new_genes, mutated)

    # Based on a mutation probability, picks a new random character
    def mutate(self, new_genes, mutation_rate):
        mutation_rate *= 100
        if randrange(0, 101) < mutation_rate:
            logging.info("mutated")
            # mutation only affects the end of the genes
            start_of_mutation = math.floor(
                len(new_genes) - (len(new_genes) * 0.2))
            for i in range(start_of_mutation, len(new_genes)):
                vec = Vector.random_2D()
                vec.limit(5000, 3000)
                new_genes[i] = vec

            return True, new_genes
        else:
            return False, new_genes
