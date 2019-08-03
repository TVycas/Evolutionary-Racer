from p5 import *
import pymunk
from dnas import DNA

collision_types = {
    "car": 1,
    "wall": 2
}


class Car:

    def __init__(self, start_point, target_line, space, num_of_forces, id):
        print("cars num = " + str(num_of_forces))
        self.space = space
        self.target_line = target_line
        self.start_point = start_point
        self.id = id
        self.w = 16
        self.h = 16
        self.max_speed = 1000
        self.max_force = 1000
        self.dna = DNA(num_of_forces, id=id)
        self.force_count = 0
        self.is_dead = False

        # Create the body with shape and add them to the space
        mass = 1
        self.points = [(-self.w / 2, -self.h / 2),
                       (0, self.h / 2), (self.w / 2, -self.h / 2)]
        # self.points_fake = [(-1, -1), (0, 1), (1, -1)]

        # moment = pymunk.moment_for_poly(mass, self.points)
        moment = 32.0

        self.body = pymunk.Body(mass, moment)
        self.body.position = start_point[0], start_point[1]

        self.shape = pymunk.Poly(self.body, self.points)
        self.shape.friction = 0.5
        self.shape.sensor = True
        self.shape.collision_type = collision_types["car"]

        self.space.add(self.body, self.shape)

        handler = space.add_collision_handler(collision_types["car"], collision_types["wall"])
        handler.begin = self.touched_wall

    def touched_wall(self, arbiter, space, data):
        car_body = arbiter.shapes[0].body
        if self.body.position == car_body.position:
            self.is_dead = True
        space.remove(car_body)
        return True

    def set_dna(self, dna):
        self.dna = dna
        self.dna.id = self.id

    def calculate_fitness(self, start_line):
        pos = (self.body.position.x, self.body.position.y)
        self.dna.calculate_fitness(pos)

    def display(self):
        pos = self.body.position
        velocity = self.body.velocity_at_world_point(pos)
        angle = velocity.angle + (PI * 1.5)

        push_matrix()
        # Using the Vector position and float angle to translate and rotate the shape
        translate(pos.x, pos.y)
        rotate(angle)
        fill(175)
        triangle(self.points[0], self.points[1], self.points[2])

        reset_matrix()

    def reset_to_start(self):
        self.body.position = self.start_point[0] + 5, self.start_point[1] + 5

        self.force_count = 0

        self.body.velocity = 0, 0

        if self.body not in self.space.bodies:
            self.space.add(self.body)

        self.is_dead = False

    # forces:
    # [+, 0] - right; [-, 0] - left
    # [0, +] - down; [0, -] - up
    def apply_force(self, force):
        self.body.apply_force_at_world_point(
            (force.x, force.y), self.body.position)

    def next_force(self):
        # TODO maybe in the DNA we should just pop the first item each time instaed of this
        # force_count
        if not self.is_dead:
            genes = self.dna.get_genes()

            if self.force_count < len(genes):
                self.apply_force(genes[self.force_count])

                pos = (self.body.position.x, self.body.position.y)
                self.dna.add_to_path_list(pos, genes[self.force_count])

                self.force_count += 1

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
