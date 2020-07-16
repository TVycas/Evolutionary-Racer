from p5 import *
import pymunk
from dnas import Dna

collision_types = {
    "car": 1,
    "wall": 2,
    "finish_line": 3
}


class Car:

    def __init__(self, map_handler, start_point, num_of_genes, end_spread, id, dna=None):
        """Creates a new car with either a given or a new Dna.

        Args:
            map_handler (MapHandler obj ): Object describing the map of the track.
            start_point (tuple): A tuple with x and y coords used to set the initial car location.
            num_of_genes (int): The number of genes in the Dna.
            end_spread (int): The number of genes to remove and replace from the end of the gene list.
            id (int): Car id.
            dna (Dna obj, optional): Object used to coordinate the evolution process. Defaults to None.
        """
        self.space = map_handler.space
        self.end_spread = end_spread
        self.finished = False
        self.is_dead = False
        self.id = id

        if dna is None:
            self.dna = Dna(map_handler.checkpoint_polys, num_of_genes, id=id)
        else:
            self.dna = dna
            self.dna.id = self.id

        self.add_new_car_to_space(start_point)
        self.add_collision_handlers()

    def add_collision_handlers(self):
        """Adds collision handlers for touching walls and reaching the finish line to the car.
        """
        handler_wall = self.space.add_collision_handler(collision_types["car"], collision_types["wall"])
        handler_wall.begin = self.touched_wall

        handler_fin = self.space.add_collision_handler(collision_types["car"], collision_types["finish_line"])
        handler_fin.begin = self.reached_finish

    def add_new_car_to_space(self, start_point, width=16, height=16, mass=1):
        """Creates a car body with a shape, based on the arguments and adds them to the pymunk physics space.

        Args:
            width (int, optional): The width of the car shape. Defaults to 16.
            height (int, optional): The height of the car shape. Defaults to 16.
            mass (int, optional): The mass of the car in space. Defaults to 1.
        """
        self.points = [(-width / 2, -height / 2),
                       (0, height / 2), (width / 2, -height / 2)]

        moment = pymunk.moment_for_poly(mass, self.points)

        self.body = pymunk.Body(mass, moment)
        self.body.position = start_point[0], start_point[1]

        shape = pymunk.Poly(self.body, self.points)
        shape.friction = 0.5
        shape.sensor = True
        shape.collision_type = collision_types["car"]

        self.space.add(self.body, shape)

    # If the car touches the wall, it's dead and no longer moves in the lifecycle
    def touched_wall(self, arbiter, space, data):
        """A car handler method that gets called when a car touches the wall.
        This removes the car from the space and marks it as "dead" (inactive).

        Args:
            arbiter (pymunk Arbiter abj): The Arbiter object encapsulates a pair of colliding shapes and all of
                                    the data about their collision.
            space (pymunk Space obj): Space describes the physics simulation space
            data (pymunk Data obj): Some extra data from the collision

        Returns:
            bool: Tells the pymunk to handle the collision normally
        """
        car_body = arbiter.shapes[0].body

        if self.body.position == car_body.position:
            self.is_dead = True

            # removes the specified amount of genes from the path list to
            # make the car possibly not hit the wall next time
            self.dna.remove_from_path_list(self.end_spread)

        space.remove(car_body)
        return True

    def reached_finish(self, arbiter, space, data):
        """A handler method to notify the system that a car has finished

        Args:
            arbiter (pymunk Arbiter abj): The Arbiter object encapsulates a pair of colliding shapes and all of
                                    the data about their collision.
            space (pymunk Space obj): Space describes the physics simulation space
            data (pymunk Data obj): Some extra data from the collision

        Returns:
            bool: Tells the pymunk to handle the collision normally
        """
        car_body = arbiter.shapes[0].body

        if self.body.position == car_body.position:
            self.finished = True
            self.is_dead = True

        space.remove(car_body)

        print("\n\nFinished!\n\n")

        return True

    def calculate_fitness(self):
        """Calculates the fitness of the car using it's Dna object"""
        pos = (int(self.body.position.x), int(self.body.position.y))
        self.dna.calculate_fitness(pos)

    def display(self):
        """Draw the car on screen.
        """
        pos = self.body.position
        velocity = self.body.velocity_at_world_point(pos)
        angle = velocity.angle + (PI * 1.5)

        with push_matrix():
            # Using the Vector position and float angle to translate and rotate the shape
            translate(pos.x, pos.y)
            rotate(angle)

            if self.dna.mutated:
                fill(255, 100, 100)
            else:
                fill(175)

            triangle(self.points[0], self.points[1], self.points[2])

    def apply_force(self, force):
        """Applies a given force Vector obj to the car.

        Args:
            force (Vector): A Vector of the force to apply.
        """

    # forces:
    # [+, 0] - right; [-, 0] - left
    # [0, +] - down; [0, -] - up
        self.body.apply_force_at_world_point(
            (force.x, force.y), self.body.position)

    def next_force(self):
        """Moves the car based on its Dna and saves its current position to the path list."""
        if not self.is_dead:
            gene = self.dna.next_gene
            if gene is not None:
                self.apply_force(gene)

                # Used to know which part of the genes were activated in which part of the track
                pos = (int(self.body.position.x), int(self.body.position.y))
                self.dna.add_to_path_list(pos, gene)
