import pymunk as pm
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


def setup():
    global cars
    global space
    global pop
    global m_handler

    rect_mode('CENTER')

    size(1000, 800)

    space = pm.Space(threaded=True)
    space.threads = 2

    m_handler = Map_handler(space, 'track.txt', 10)

    pop = Population(lifespan, m_handler, 50, 0.3, 25)


def draw():
    global cars
    global life_counter
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
