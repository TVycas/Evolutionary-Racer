import pymunk as pm
from p5 import *
from cars import collision_types
from shapely.geometry.polygon import Polygon
from file_reader import read_track_files


class Map_handler:

    def __init__(self, space, track_file, start_finish_offset):
        self.space = space
        self.wall_segs = read_track_files(track_file)
        self.walls = []
        self.endpoints = []

        for i in range(0, len(self.wall_segs), 2):
            self.walls += self.create_wall_segments(
                (self.wall_segs[i], self.wall_segs[i + 1]), collision_types["wall"])

        self.checkpoint_polys = self.create_checkpoint_polys()

        self.num_of_walls = len(self.space.bodies)

        self.starting_line, self.finish_line = self.create_finish_start_lines(
            start_finish_offset)

        # creates invisible finish line
        self.create_invisible_line(self.finish_line)

    def create_invisible_line(self, line):
        self.create_wall_segments(line, collision_types["finish_line"])

    def create_finish_start_lines(self, offset):
        finish_line_on_map = [self.wall_segs[-2], self.wall_segs[-1]]

        first_point = list(finish_line_on_map[0])
        second_point = list(finish_line_on_map[1])

        for i in range(len(first_point)):
            first_point[i] += offset
            second_point[i] += offset

        start_line = [tuple(first_point), tuple(second_point)]

        for i in range(len(first_point)):
            first_point[i] -= offset * 2
            second_point[i] -= offset * 2

        finish_line = [tuple(first_point), tuple(second_point)]

        return start_line, finish_line

    def draw_checkpoint_polys(self):
        for poly in self.checkpoint_polys:
            poly_coords = list(poly.exterior.coords)

            fill(0)
            quad(poly_coords[0], poly_coords[1],
                 poly_coords[2], poly_coords[3])

    def create_checkpoint_polys(self):
        polys = []
        points = []
        for checkpoint in self.wall_segs:
            points.append(checkpoint)
            if len(points) == 4:
                polys.append(
                    Polygon([points[1], points[0], points[2], points[3]]))
                points = points[2:]
        return polys

    def draw_walls(self):
        if len(self.walls) < 1:
            return

        for wall_seg in self.walls:
            body = wall_seg.body
            pv1 = body.position + wall_seg.a.rotated(body.angle)  # 1
            pv2 = body.position + wall_seg.b.rotated(body.angle)
            p1 = (int(pv1.x), int(pv1.y))
            p2 = (int(pv2.x), int(pv2.y))

            fill(0)
            line(p1, p2)

    def create_wall_segments(self, points, coll_type):
        """Create a number of wall segments connecting the points"""
        walls = []
        if len(points) < 2:
            return []

        points = list(map(pm.Vec2d, points))
        for i in range(len(points) - 1):
            v1 = pm.Vec2d(points[i].x, points[i].y)
            v2 = pm.Vec2d(points[i + 1].x, points[i + 1].y)

            wall_body = pm.Body(body_type=pm.Body.STATIC)
            wall_shape = pm.Segment(wall_body, v1, v2, .0)
            wall_shape.friction = 0.5
            wall_shape.collision_type = coll_type

            self.space.add(wall_shape)
            walls.append(wall_shape)

        return walls

    def add_wall(self, wall_to_add):
        self.walls += self.create_wall_segments(wall_to_add, collision_types["wall"])

    def add_endpoint(self, endpoint):
        self.endpoints.append(endpoint)

    def draw_endpoints(self, num_endpoints_to_draw):
        self.endpoints = self.endpoints[-num_endpoints_to_draw:]
        for point in self.endpoints:
            fill(255, 204, 0)
            circle(point, 5)
