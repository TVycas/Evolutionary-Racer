# A class to describe a pseudo-DNA, i.e. genotype
#   Here, a virtual organism's DNA is an array of character.
#   Functionality:
#      -- convert DNA into a string
#      -- calculate DNA's "fitness"
#      -- mate DNA with another set of DNA
#      -- mutate DNA
import math
from p5 import *
from random import randrange, choice
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from file_reader import read_track_files


class DNA:

    # makes a random DNA
    def __init__(self, num, genes=None, id=-1):
        # print("dna num = " + str(num))
        self.fitness = 0
        self.polys = self.create_checkpoint_polys(read_track_files(
            'checkpoints.txt'))
        self.path_list = []
        self.farthest_poly_reached = 0
        self.id = id

        # if self.id == 0:
        #     self.genes = read_track_files('vectors0.txt')
        # elif self.id == 1:
        #     self.genes = read_track_files('vectors1.txt')
        # elif self.id == 2:
        #     self.genes = read_track_files('vectors2.txt')
        # elif self.id == 3:
        #     self.genes = read_track_files('vectors3.txt')
        # for i, vec in enumerate(self.genes):
        #     self.genes[i] = Vector(vec[0], vec[1])



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

    def create_checkpoint_polys(self, checkpoints):
        # todo refactor to sketch?
        polys = []

        points = []
        for checkpoint in checkpoints:
            points.append(checkpoint)

            if len(points) == 4:
                polys.append(
                    Polygon([points[0], points[1], points[2], points[3]]))

                points = points[2:]

        return polys

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

        # print("fitness = " + str(self.fitness))

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

        print("\nMy id = " + str(self.id) + " my partner's id = " + str(partner.id))

        # print("\nmy_path_list - " + str(self.id) + "\n")
        # for i, lst in enumerate(self.path_list):
        #     print("#" + str(i))
        #     for gene in lst:
        #         print(gene)

        # print("\npartner_path_list - " + str(partner.id) + "\n")
        # for i, lst in enumerate(partner.path_list):
        #     print("#" + str(i))
        #     for gene in lst:
        #         print(gene)

        # print("\nboth genes \n")
        # for i, gene in enumerate(self.genes):
        #     print(str(gene) + " - " + str(partner.genes[i]))

        for i, gene_block in enumerate(self.path_list):
            if len(partner.path_list[i]) == 0 and len(gene_block) == 0:
                break

            new_genes.extend(choice([gene_block, partner.path_list[i]]))
            # if self.fitness > partner.fitness:
            #     new_genes.extend(gene_block)
            # else:
            #     new_genes.extend(partner.path_list[i])

            if new_genes == gene_block:
                print("chosen block from id = " + str(self.id))
            else:
                print("chosen block from id = " + str(partner.id))

        self.mutate(new_genes, mutation_rate)

        # Pad the rest of the genes with random vectors
        while len(new_genes) < len(self.genes):
            # print("adds random vector")
            vec = Vector.random_2D()
            vec.limit(5000, 3000)
            new_genes.append(vec)

        while len(new_genes) > len(self.genes):
            # print("removes vector")
            new_genes.pop()

        # print("\nnew_genes\n")
        # for gene in new_genes:
        #     print(gene)


        return DNA(len(self.genes), new_genes)

    # Based on a mutation probability, picks a new random character
    def mutate(self, genes, mutation_rate):
        mutation_rate *= 100
        if randrange(0, 101) < mutation_rate:
            print("mutated")
            # mutation only affects the end of the genes
            start_of_mutation = math.floor(len(genes) - (len(genes) * 0.3))
            for i in range(start_of_mutation, len(genes)):
                vec = Vector.random_2D()
                vec.limit(5000, 3000)
                genes[i] = vec

            return genes
