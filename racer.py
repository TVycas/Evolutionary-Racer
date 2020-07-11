import pymunk as pm
import datetime
import sys
import getopt
from map_handlers import Map_handler
from p5 import *
from populations import Population

space = None
cars = []
ctrl_key_pressed = False  # l for now
pop = None
lifespan = 1500
life_counter = 0
display_checkpoint_polys = False
map_handler = None
start_time = 0
end_time = 0
finished = False
# Default parameters
mut_rate = 0.3
pop_size = 20
track_file = 'track.txt'


def parse_args():
    global mut_rate
    global pop_size
    global track_file

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(
            argv, "m:p:t:", ["mut_rate=", "pop_size=", "track_file="])
    except getopt.GetoptError:
        print('usage: sketch.py -p <population_size> -m <mutation_rate>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mut_rate"):
            try:
                mut_rate = float(arg)
            except:
                print("\nMutation rate needs to be a float")
        elif opt in ("-p", "--pop_size"):
            try:
                pop_size = int(arg)
            except:
                print("\nPopulation size needs to be an integer")
        elif opt in ("-t", "--track_file"):
            track_file = arg

    print(f"\nRunning with - \nPoplation size = {pop_size}" +
          f"\nMutation rate = {mut_rate}\nTrack file = {track_file}")


def setup():
    global space
    global pop
    global start_time
    global map_handler

    parse_args()
    # Set up the screen
    rect_mode('CENTER')
    size(1000, 800)

    # Set up the physics space
    space = pm.Space(threaded=True)
    space.threads = 2

    # Set up the map_handler for map-related calculations and drawing
    map_handler = Map_handler(space, track_file, 10)

    # Set up the population object to run the algorithm
    pop = Population(lifespan, map_handler, 50, mut_rate, pop_size)

    start_time = datetime.datetime.now()


def draw():
    global life_counter
    global end_time
    global finished

    # Check if the conditions for the end of an epoch are met, and if so, run the genetic algorithm
    life_counter += 1
    if (life_counter == lifespan or len(space.bodies) == map_handler.num_of_walls) and not finished:
        life_counter = 0
        pop.calculate_fitness()
        pop.natural_selection()
        map_handler.add_endpoint(pop.evaluate())
        pop.generate()

    # Update the physics
    space.step(1 / 100.0)

    # Draw background
    background(255)

    # Draw walls
    map_handler.draw_walls()

    # Draw endpoints (the n best positions reached so far)
    map_handler.draw_endpoints(5)

    # Draw and update the cars
    finished = pop.update_and_draw_cars()

    # If finished, display info about the run (time and the number of generations it took)
    if finished:
        if end_time == 0:
            end_time = datetime.datetime.now()
            time_taken = end_time - start_time

        text('Time taken to finish the track - ' + str(time_taken).split('.', 2)
             [0] + ' Generations - ' + str(pop.generations), ((width / 2) - 20, height / 2), 25)

        no_loop()

    title(f"Frame Rate: {frame_rate}")

    # Draws black boxes to indicate checkpoints areas
    if display_checkpoint_polys:
        map_handler.draw_checkpoint_polys()


def mouse_pressed():
    global wall_to_add

    if ctrl_key_pressed:
        wall_to_add = []
        wall_to_add.append((mouse_x, mouse_y))


def mouse_released():
    global wall_to_add

    wall_end_tpl = (mouse_x, mouse_y)

    if ctrl_key_pressed and not wall_to_add[0] == wall_end_tpl:
        wall_to_add.append(wall_end_tpl)
        map_handler.add_wall(wall_to_add)

        print(f"New wall added at coods: {wall_to_add[0]} - {wall_end_tpl}")


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
