import pymunk as pm
import sys
from p5 import *
from cars import collision_types
from shapely.geometry.polygon import Polygon


class MapHandler:

    def __init__(self, space, map_file, start_finish_offset):
        self.space = space
        self.wall_points = MapHandler.read_map_file(map_file)
        self.walls = []
        self.endpoints = []

        for i in range(0, len(self.wall_points), 2):
            wall = (self.wall_points[i], self.wall_points[i + 1])
            self.walls += self.create_wall_segments(wall, collision_types["wall"])

        self.checkpoint_polys = self.create_checkpoint_polys()

        self.num_of_walls = len(self.space.bodies)

        self.starting_line, self.finish_line = self.create_finish_start_lines(
            start_finish_offset)

        # Creates an invisible finish line
        self.create_wall_segments(self.finish_line, collision_types["finish_line"])

    def create_finish_start_lines(self, offset):
        """Calculates the start and finish lines of the track. The finish line is
        calculated by subtracting the offset from the start line.

        Args:
            offset (int): The offset of pixels the finish line is before the start line.

        Returns:
            tuple: Start line of the track.
            tuple: Finish line of the track.
        """
        finish_line_on_map = [self.wall_points[-2], self.wall_points[-1]]

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
        num_of_colours = int(255 / len(self.checkpoint_polys))

        for index, poly in enumerate(self.checkpoint_polys):
            poly_coords = list(poly.exterior.coords)

            colour = Color(index * num_of_colours)
            colour.alpha = 100
            fill(colour)

            quad(poly_coords[0], poly_coords[3],
                 poly_coords[2], poly_coords[1])

    def create_checkpoint_polys(self):
        """Calculates a list of Polygon objects that describe the checkpoints of the track
        based on the wall connections in the map file.

        Returns:
            list: List of Polygon objects
        """
        polys = []

        for point_index in range(0, len(self.wall_points) - 2, 4):  # We don't want to include the finish/start line
            polys.append(Polygon([self.wall_points[point_index],
                                 self.wall_points[point_index + 2],
                                 self.wall_points[point_index + 3],
                                 self.wall_points[point_index + 1]]))

        return polys

    def draw_walls(self):
        """Draws the walls on the map."""

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
        """Creates a number of wall segments connecting the wal points in the map file."""
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
        """Adds a wall to the map.

        Args:
            wall_to_add (tuple): A tuple of points describing a new wall.
        """
        self.walls += self.create_wall_segments(wall_to_add, collision_types["wall"])

    def draw_endpoints(self, num_endpoints_to_draw):
        """Draws a number of cirles indicating the furthest location the cars reached
        over previous generations.

        Args:
            num_endpoints_to_draw (int): The number of endpoints to draw.
        """
        self.endpoints = self.endpoints[-num_endpoints_to_draw:]
        for point in self.endpoints:
            fill(255, 204, 0)
            circle((point), 5)

    @staticmethod
    def find_line_midpoint(line):
        """A helper method that calculates the midpoint of a line.

        Args:
            line (tuple): A tuple of points describing a line.

        Returns:
            tuple: A tuple of coords that are the middle of the line on the map.
        """
        xs_avg = (line[0][0] + line[1][0]) / 2
        ys_avg = (line[0][1] + line[1][1]) / 2
        return (xs_avg, ys_avg)

    @staticmethod
    def read_map_file(file):
        """Reads the map from a given file.

        Args:
            file (str): The location and name of the map file.

        Returns:
            list: list of points describing the walls read.
        """

        read_walls = []
        try:
            track_walls = np.genfromtxt(file, delimiter=',', comments='#')
        except IOError:
            print("Track file is not working")
            sys.exit(2)

        read_wall_points = []
        count = 0
        for wall in track_walls:
            count += 1

            read_wall_points.append((wall[0], wall[1]))

            if count == 2:
                read_walls += read_wall_points
                read_wall_points = []
                count = 0

        return read_walls
