import pymunk as pm
from p5 import *
from cars import collision_types

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

    #TODO this shouldn't be hard-codded
    # finish line
    fill(0)
    line((364, 519), (364, 591))


def draw_checkpoint_blocks(checkpoint_blocks):
    points = []
    for checkpoint in checkpoint_blocks:
        points.append(checkpoint)

        if len(points) == 4:
            fill(0)
            quad(points[0], points[1], points[2], points[3])
            points = points[2:]


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
