import pymunk as pm
from p5 import *
from cars import collision_types
from shapely.geometry.polygon import Polygon


def create_finish_start_lines(finish_line_on_map, offset):
    if len(finish_line_on_map) < 2:
        return []

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


def draw_checkpoint_polys(polys):
    for poly in polys:
        poly_coords = list(poly.exterior.coords)

        fill(0)
        quad(poly_coords[0], poly_coords[1], poly_coords[2], poly_coords[3])


def create_checkpoint_polys(map_segs):
    polys = []
    points = []
    for checkpoint in map_segs:
        points.append(checkpoint)
        if len(points) == 4:
            polys.append(
                Polygon([points[1], points[0], points[2], points[3]]))
            points = points[2:]
    return polys


def draw_walls(walls):
    if len(walls) < 1:
        return

    for wall_seg in walls:
        body = wall_seg.body
        pv1 = body.position + wall_seg.a.rotated(body.angle)  # 1
        pv2 = body.position + wall_seg.b.rotated(body.angle)
        p1 = (int(pv1.x), int(pv1.y))
        p2 = (int(pv2.x), int(pv2.y))

        fill(0)
        line(p1, p2)


def create_wall_segments(space, points):
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
        wall_shape.collision_type = collision_types["wall"]

        space.add(wall_shape)
        walls.append(wall_shape)

    return walls
