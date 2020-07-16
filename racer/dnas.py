
import math
import random
from p5 import *
from random import randrange, choice
from shapely.geometry import Point


class Dna:

    def __init__(self, checkpoint_polys, num_of_genes, genes=None, mutated=False, id=-1):
        """The init can either create a random or specific Dna object

        Args:
            checkpoint_polys (list of Polygon obj): A list of polygons describing the checkpoints in the track.
            num_of_genes (int): The number of genes for the Dna to have.
            genes (list of Vector obj, optional): A list of genes to create the Dna obj from. Defaults to None.
            mutated (bool, optional): A bool to note if the Dna muteted. Defaults to False.
            id (int, optional): The id of the Dna obj. Defaults to -1.
        """

        self.fitness = 0
        self.checkpoint_polys = checkpoint_polys
        self.path_list = []
        self.farthest_poly_reached = 0
        self.id = id
        self.num_of_genes = num_of_genes
        self.mutated = mutated

        self.max_checkpnt_len = width if width > height else height

        # Add enough empty lists to the path_list so that the vectors in genes could be
        # divided to each polygon
        for i in range(0, len(self.checkpoint_polys)):
            self.path_list.append([])

        if genes is None:
            # The genetic sequence
            self.genes = []
            for x in range(0, int(num_of_genes)):
                vec = Vector.random_2D()
                vec.limit(5000, 3000)
                self.genes.append(vec)
        else:
            self.genes = genes

    def calculate_fitness(self, pos):
        """Calculates the fitness of the Dna. The fitness is calculated based
        on the distance to the next checkpoint of the map.

        Args:
            pos (tuple): A tuple cooresponding to the possition of the car.
        """

        # First, the number checkpoints reached so far is calculated, then
        # the distance to the next checkpoint line is added. For greater differences between
        # fitnesses, the resulting number is cubed.

        self.fitness = self.find_current_checkpoint(pos)

        if self.fitness != -1:
            dist_to_next_chpt = self.find_dist_to_next_chpt(
                pos, self.checkpoint_polys[self.fitness])

            self.fitness += 1 - remap(dist_to_next_chpt, (0, self.max_checkpnt_len), (0, 1))
            self.fitness *= self.fitness * self.fitness

    def find_current_checkpoint(self, pos):
        """Finds the checkpoint polygon that the car is in.

        Args:
            pos (tuple): A tuple cooresponding to the possition of the car.

        Returns:
            [int]: The ID of the checkpoint polygon in witch he car is in.
        """

        position = Point(pos)

        current_checkpoint_id = -1
        for i, poly in enumerate(self.checkpoint_polys):
            if poly.contains(position):
                current_checkpoint_id = i
                break

        return current_checkpoint_id

    def find_dist_to_next_chpt(self, pos, current_polygon):
        """Calculates the distance to the next checkpoint polygon

        Args:
            pos (tuple): tuple describing the current car position
            current_polygon (int): the ID of the polygon in witch the car is in

        Returns:
            float: The distance to the next checkpoint polygon
        """

        # |AC x AB| / |AB| where AB is the line and C is the point
        # Calculates the distace to the next checkpoint polygon using the formula above.
        current_poly_coords = list(current_polygon.exterior.coords)

        ab = Dna.vector_from_two_points(
            current_poly_coords[2], current_poly_coords[3])

        ac = Dna.vector_from_two_points(current_poly_coords[2], pos)

        ac_ab_cross = ac.cross(ab)

        magnitude_of_ac_ab_cross = ac_ab_cross.magnitude
        magnitude_of_ab = ab.magnitude

        distance = magnitude_of_ac_ab_cross / magnitude_of_ab

        return distance

    @property
    def next_gene(self):
        if len(self.genes) > 0:
            return self.genes.pop(0)
        else:
            return None

    @staticmethod
    def vector_from_two_points(point1, point2):
        x = point2[0] - point1[0]
        y = point2[1] - point1[1]
        return Vector(x, y)

    def add_to_path_list(self, pos, current_gene):
        """Update the path list to track the possition of the car, if the car has not turned around.

        Args:
            pos (tuple): The current position of the car
            current_vector (Vector object): The gene that the car was just moved by
        """

        current_checkpoint = self.find_current_checkpoint(pos)

        if self.farthest_poly_reached <= current_checkpoint:
            self.farthest_poly_reached = current_checkpoint
            self.path_list[current_checkpoint].append(current_gene)
        # If the car turns around, we don't want to save that
        elif self.farthest_poly_reached > current_checkpoint:
            return

    def remove_from_path_list(self, num_vec_to_remove):
        """Removes a specified amount of genes from the end of the gene list
        to help map exploration.

        Args:
            num_vec_to_remove (int): number of genes to remove
        """

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

        for i, gene_block in enumerate(self.path_list):
            if len(partner.path_list[i]) == 0 and len(gene_block) == 0:
                # If both of the parters don't have genes for the current gene block, top the crossover.
                break

            # Chose the parent of the next gene block randomly.
            new_genes.extend(choice([gene_block, partner.path_list[i]]))

        mutated, new_genes = self.mutate(new_genes, mutation_rate)
        new_genes = self.normalize_gene_list(new_genes)

        return Dna(self.checkpoint_polys, self.num_of_genes, new_genes, mutated)

    def normalize_gene_list(self, genes):
        """Add or remove additional genes if the length of the gene list
        is too big or small.

        Args:
            genes (list of Vector obj): The list of genes

        Returns:
            (list of Vector obj): The list of genes at the correct length
        """

        while len(genes) < self.num_of_genes:
            vec = Vector.random_2D()
            vec.limit(5000, 3000)
            genes.append(vec)

        while len(genes) > self.num_of_genes:
            genes.pop()

        return genes

    def mutate(self, genes, mutation_rate):
        """Mutate 10 to 30 percent of the last genes in the genes by replacing
        the genes with new random values.

        Args:
            genes (list of Vector obj): The list of genes
            mutation_rate (float): The rate of mutation

        Returns:
            (bool): Whether the mutation happened.
            (list of Vector obj): The list of new, possibly mutated, genes
        """

        mutation_rate *= 100
        if randrange(0, 101) < mutation_rate:
            # mutation only affects the end of the genes
            affected_genes = random.uniform(0.1, 0.3)
            start_of_mutation = math.floor(len(genes) - (len(genes) * affected_genes))
            for i in range(start_of_mutation, len(genes)):
                vec = Vector.random_2D()
                vec.limit(5000, 3000)
                genes[i] = vec

            return True, genes
        else:
            return False, genes
