import numpy as np


def read_file():
    with open('input.txt', 'r') as f:
        text = [f.strip() for f in f.readlines()]
    tuples = [[list(map(int, coord_pair.split(','))) for coord_pair in line.split(' -> ')] for line in text]
    return np.asarray(tuples)


def get_map(horz_vert: bool = False):
    coords = read_file()
    if horz_vert:
        horz_vert_lines = np.where((coords[:, 0, 0] == coords[:, 1, 0]) | (coords[:, 0, 1] == coords[:, 1, 1]))
        coords = coords[horz_vert_lines]

    max_value = np.max(coords) + 1
    field = np.zeros((max_value, max_value))
    for ((x1, y1), (x2, y2)) in coords:
        xs = list(range(x1, x2, 1 if x1 < x2 else -1)) + [x2]
        ys = list(range(y1, y2, 1 if y1 < y2 else -1)) + [y2]

        field[(xs, ys)] += 1

    return field


def part_one():
    return np.where(get_map(True) > 1)[0].shape


def part_two():
    return np.where(get_map() > 1)[0].shape


print(part_one())
print(part_two())
