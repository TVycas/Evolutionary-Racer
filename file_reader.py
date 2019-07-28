import numpy as np


def read_track_files(file):
    read_walls = []
    track_walls = np.genfromtxt(file, delimiter=',', comments='#')

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
