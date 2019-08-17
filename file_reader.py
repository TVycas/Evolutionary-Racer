import numpy as np
import sys

# TODO move to map_handler?
def read_track_files(file):
    read_walls = []
    try:
        track_walls = np.genfromtxt(file, delimiter=',', comments='#')
    except:
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
