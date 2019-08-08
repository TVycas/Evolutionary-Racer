from p5 import *
import pymunk
from dnas import DNA

collision_types = {
    "car": 1,
    "wall": 2
}


class Car:

    def __init__(self, m_handler, start_point, num_of_forces, end_spread, id, dna=None):
        self.space = m_handler.space

        self.finish_line = m_handler.finish_line
        self.start_point = start_point
        self.end_spread = end_spread

        self.id = id

        self.w = 16
        self.h = 16

        self.max_speed = 1000
        self.max_force = 1000

        if dna is None:
            self.dna = DNA(m_handler.checkpoint_polys, num_of_forces, id=id)
        else:
            self.dna = dna
            self.dna.id = self.id

        self.is_dead = False

        # Create the body with shape and add them to the space
        mass = 1
        self.points = [(-self.w / 2, -self.h / 2),
                       (0, self.h / 2), (self.w / 2, -self.h / 2)]

        moment = pymunk.moment_for_poly(mass, self.points)

        self.body = pymunk.Body(mass, moment)
        self.body.position = start_point[0], start_point[1]

        self.shape = pymunk.Poly(self.body, self.points)
        self.shape.friction = 0.5
        self.shape.sensor = True
        self.shape.collision_type = collision_types["car"]

        self.space.add(self.body, self.shape)

        handler = self.space.add_collision_handler(collision_types["car"], collision_types["wall"])
        handler.begin = self.touched_wall

    # If the car touches the wall, it's dead and no longer moves in the lifecycle
    def touched_wall(self, arbiter, space, data):
        car_body = arbiter.shapes[0].body

        if self.body.position == car_body.position:
            self.is_dead = True
            # removes the specified amount of vectors from the path list to
            # make the car possibly not hit the wall next time
            self.dna.remove_from_path_list(self.end_spread)

        space.remove(car_body)
        return True

    def calculate_fitness(self):
        pos = (self.body.position.x, self.body.position.y)
        self.dna.calculate_fitness(pos)

    def display(self):
        pos = self.body.position
        velocity = self.body.velocity_at_world_point(pos)
        angle = velocity.angle + (PI * 1.5)

        with push_matrix():
            # Using the Vector position and float angle to translate and rotate the shape
            translate(pos.x, pos.y)
            rotate(angle)
            fill(175)
            triangle(self.points[0], self.points[1], self.points[2])

    # forces:
    # [+, 0] - right; [-, 0] - left
    # [0, +] - down; [0, -] - up
    def apply_force(self, force):
        self.body.apply_force_at_world_point(
            (force.x, force.y), self.body.position)

    def next_force(self):
        if not self.is_dead:
            gene = self.dna.get_next_gene()
            if gene is not None:
                self.apply_force(gene)

                pos = (self.body.position.x, self.body.position.y)
                self.dna.add_to_path_list(pos, gene)
            # else:
            #     self.is_dead = True
            #     self.space.remove(self.shape)
            #     self.space.remove(self.body)


# #############################Unused#################################################
    def seek(self, target):
        pos = self.body.position
        position_vec = self.vec2d_to_vector(pos)

        desired = Vector(target[0], target[1]) - position_vec
        desired.normalize()
        desired *= self.max_speed

        vel = self.vec2d_to_vector(self.body.velocity_at_world_point(pos))

        steer = desired - vel
        steer.limit(self.max_force)

        self.apply_force(steer)

    @staticmethod
    def vec2d_to_vector(vec2d):
        return Vector(vec2d.x, vec2d.y)

    # def arrive(self, target):
    #     pos = self.body.position
    #     position_vec = car.vec2d_to_vector(pos)

    #     velocity = car.vec2d_to_vector(self.body.velocity_at_world_point(pos))
    #     velocity_mag = velocity.magnitude

    #     desired = Vector(target[0], target[1]) - position_vec
    #     desired_mag = desired.magnitude
    #     desired.normalize()

    #     if desired_mag < 100:
    #         m = remap(desired_mag, (0, 99), (0, -velocity_mag))

    #         desired *= m
    #     else:
    #         desired *= self.max_speed

    #     vel = car.vec2d_to_vector(self.body.velocity_at_world_point(pos))

    #     steer = desired - vel
    #     steer.limit(self.max_force)

    #     car.apply_force(self, [steer.x, steer.y])
