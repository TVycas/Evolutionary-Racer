import pymunk as pm
import map_handler as map_handler
from p5 import *
from file_reader import read_track_files
from populations import Population

from shapely.geometry.polygon import Polygon

space = None
cars = []
walls = []
ctrl_key_pressed = False  # l for now
wall_to_add = []
pop = None
lifespan = 500
life_counter = 0
checkpoint_polys = None
display_checkpoint_polys = False
num_of_walls = 0

end_points = []

def setup():
    global cars
    global space
    global pop
    global walls
    global checkpoint_polys
    global num_of_walls

    rect_mode('CENTER')

    size(1000, 800)

    space = pm.Space(threaded=True)
    space.threads = 2

    # Invisible wall between start and finish so that the cars wouldn't
    # go backwards
    map_handler.create_wall_segments(space, ((363, 519), (363, 591)))

    # Load and create the track
    wall_segs = read_track_files('track.txt')
    for i in range(0, len(wall_segs), 2):
        walls += map_handler.create_wall_segments(space, (wall_segs[i], wall_segs[i + 1]))

    # For displaying the checkpoints
    checkpoint_polys = map_handler.create_checkpoint_polys(wall_segs)

    num_of_walls = len(space.bodies)

    starting_line, finish_line = map_handler.create_finish_start_lines([wall_segs[-2], wall_segs[-1]], 10)

    pop = Population(space, lifespan, starting_line, finish_line, 0.3, 20)


def draw():
    global cars
    global life_counter
    global end_points

    life_counter += 1
    if life_counter == lifespan or len(space.bodies) == num_of_walls:
        life_counter = 0
        pop.calculate_fitness()
        pop.natural_selection()
        end_points.append(pop.evaluate())
        pop.generate()

    space.step(1 / 100.0)

    background(255)

    # Draw walls
    map_handler.draw_walls(walls)

    # draw ends points
    end_points = end_points[-5:]
    for point in end_points:
        fill(255, 204, 0)
        circle(point, 5)

    pop.draw_cars(mouse_x, mouse_y)

    title("Frame Rate: " + str(frame_rate))

    # Draws black boxes to indicate the checkpoint area
    if display_checkpoint_polys:
        map_handler.draw_checkpoint_polys(checkpoint_polys)


def mouse_pressed():
    global ctrl_key_pressed
    global wall_to_add

    if ctrl_key_pressed:
        wall_to_add = []
        wall_to_add.append((mouse_x, mouse_y))


def mouse_released():
    global wall_to_add
    global walls
    if ctrl_key_pressed:
        wall_to_add.append((mouse_x, mouse_y))
        walls += map_handler.create_wall_segments(space, wall_to_add)
        print("new wall")
        for wall in wall_to_add:
            print(wall)


def key_pressed(event):
    global ctrl_key_pressed
    global display_checkpoint_polys

    if event.key == 'L':
        print("Drawing walls toggled")
        ctrl_key_pressed = not ctrl_key_pressed
    elif event.key == 'C':
        print("Display checkpoint blocks toggled")
        display_checkpoint_polys = not display_checkpoint_polys


if __name__ == "__main__":
    run()