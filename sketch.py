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
m_handler = None
finished = False
start_time = 0
end_time = 0
time_taken = 0
# Default values
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

    print("\nRunning with - \nPoplation size = " + str(pop_size) +
          "\nMutation rate = " + str(mut_rate) + "\nTrack file = " + track_file)


def setup():
    global cars
    global space
    global pop
    global start_time
    global m_handler

    parse_args()
    rect_mode('CENTER')

    size(1000, 800)

    space = pm.Space(threaded=True)
    space.threads = 2

    m_handler = Map_handler(space, track_file, 10)

    pop = Population(lifespan, m_handler, 50, mut_rate, pop_size)

    start_time = datetime.datetime.now()


def draw():
    global cars
    global life_counter
    global end_time
    global time_taken
    global finished

    life_counter += 1
    if (life_counter == lifespan or len(space.bodies) == m_handler.num_of_walls) and not finished:
        life_counter = 0
        pop.calculate_fitness()
        pop.natural_selection()
        m_handler.add_endpoint(pop.evaluate())
        pop.generate()

    space.step(1 / 100.0)

    background(255)

    # Draw walls
    m_handler.draw_walls()

    # draw ends points
    m_handler.draw_endpoints(5)

    finished = pop.draw_cars(mouse_x, mouse_y)

    if finished:
        if end_time == 0:
            end_time = datetime.datetime.now()
            time_taken = end_time - start_time

        text('Time taken to finish the track - ' + str(time_taken).split('.', 2)
             [0] + ' Generations - ' + str(pop.generations), ((width / 2) - 20, height / 2), 25)

        no_loop()

    title("Frame Rate: " + str(frame_rate))

    # Draws black boxes to indicate the checkpoint area
    if display_checkpoint_polys:
        m_handler.draw_checkpoint_polys()


def mouse_pressed():
    global ctrl_key_pressed
    global wall_to_add

    if ctrl_key_pressed:
        wall_to_add = []
        wall_to_add.append((mouse_x, mouse_y))


def mouse_released():
    global wall_to_add

    if ctrl_key_pressed:
        wall_to_add.append((mouse_x, mouse_y))
        m_handler.add_wall(wall_to_add)
        print(wall_to_add[0])
        print(wall_to_add[1])


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
