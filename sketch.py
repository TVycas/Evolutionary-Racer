import pymunk as pm
from p5 import *
from file_reader import read_track_files
from populations import Population
from cars import collision_types

space = None
cars = []
walls = []
ctrl_key_pressed = False  # l for now
wall_to_add = []
pop = None
lifespan = 300
life_counter = 0
checkpoints = []
checkpoint_blocks = None
display_checkpoint_blocks = False
num_of_walls = 0


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


def create_wall_segments(points):
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


def draw_checkpoint_blocks():
    points = []
    for checkpoint in checkpoint_blocks:
        points.append(checkpoint)

        if len(points) == 4:
            fill(0)
            quad(points[0], points[1], points[2], points[3])
            points = points[2:]


def setup():
    global cars
    global space
    global pop
    global walls
    global checkpoint_blocks
    global num_of_walls

    rect_mode('CENTER')

    size(1000, 800)

    space = pm.Space(threaded=True)
    space.threads = 2

    # Invisible wall between start and finish so that the cars wouldn't
    # go backwards
    create_wall_segments([(363, 519), (363, 591)])

    # For displaying the checpoints
    checkpoint_blocks = read_track_files('checkpoints.txt')

    # Load and create the track
    wall_segs = read_track_files('track.txt')
    for i in range(0, len(wall_segs), 2):
        walls += create_wall_segments([wall_segs[i], wall_segs[i + 1]])

    num_of_walls = len(space.bodies)

    finish_line = [(360, 519), (360, 591)]
    starting_line = [(375, 519), (375, 591)]
    pop = Population(space, lifespan, starting_line, finish_line, 0.2, 15)


def draw():
    global cars
    global life_counter
    global draw_checkpoint_blocks

    life_counter += 1
    if life_counter == lifespan or len(space.bodies) == num_of_walls:
        life_counter = 0
        pop.calculate_fitness()
        pop.natural_selection()
        pop.evaluate()
        pop.generate()

    space.step(1 / 300.0)

    background(255)

    if display_checkpoint_blocks:
        draw_checkpoint_blocks()

    # finish line
    fill(0)
    line((364, 519), (364, 591))

    # track walls
    draw_walls(walls)

    print((life_counter % 10))
    if (life_counter % 10) == 0:
        print(life_counter)
        pop.apply_force = True

    pop.draw_cars(mouse_x, mouse_y)


def mouse_pressed():
    global ctrl_key_pressed
    global wall_to_add

    if ctrl_key_pressed:
        wall_to_add = []
        wall_to_add.append((mouse_x, mouse_y))
    else:
        #cars.append(car(mouse_x, mouse_y, space, width, height))
        print(frame_rate)


def mouse_released():
    global wall_to_add
    global walls
    if ctrl_key_pressed:
        wall_to_add.append((mouse_x, mouse_y))
        walls += create_wall_segments(wall_to_add)
        print("new wall")
        for wall in wall_to_add:
            print(wall)


def key_pressed(event):
    global ctrl_key_pressed
    global display_checkpoint_blocks

    if event.key == 'L':
        print("Drawing walls toggled")
        ctrl_key_pressed = not ctrl_key_pressed
    elif event.key == 'C':
        print("Display checkpoint blocks toggled")
        display_checkpoint_blocks = not display_checkpoint_blocks


if __name__ == "__main__":
    run()
