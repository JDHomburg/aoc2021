import numpy as np

from functions.data_in import read_data


def format_data(file_path='input.txt'):
    result = list()
    for line in read_data(file_path):
        on_off, cube = line.split(' ')
        x_y_z = cube.split(',')
        result.append((on_off == 'on',
                       [list(map(int, v.split('=')[1].split('..'))) for v in x_y_z]))
    return result


def run_sequence(actions):
    idxs = [value for action in actions if action[1] for xyz in action[1] for value in xyz]
    size = max(idxs) - min(idxs) + 1
    offset = -min(idxs)
    cubes = np.zeros((size, size, size), dtype=np.bool_)
    for value, (x, y, z) in actions:
        cubes[
        x[0] + offset:x[1] + offset + 1,
        y[0] + offset:y[1] + offset + 1,
        z[0] + offset:z[1] + offset + 1
        ] = value
    return cubes


def run_sequences_set(actions):
    cube = set()
    for value, ((min_x, max_x), (min_y, max_y), (min_z, max_z)) in actions:
        coordinates = {(x, y, z)
                       for x in range(min_x, max_x + 1)
                       for y in range(min_y, max_y + 1)
                       for z in range(min_z, max_z + 1)}
        if value:
            cube = cube.union(coordinates)
        else:
            cube = cube.difference(coordinates)
    return cube


def run_sequences_cube(actions):
    cubes = list()
    for value, cube in actions:
        new_cubes = list()
        for cube_ in cubes:
            if any([coord_min_ > coord_max or coord_min > coord_max_
                    for (coord_min, coord_max), (coord_min_, coord_max_) in zip(cube, cube_)]):
                new_cubes.append(cube_)
                continue
            (c1_x_min, c1_x_max), (c1_y_min, c1_y_max), (c1_z_min, c1_z_max) = cube_
            (c2_x_min, c2_x_max), (c2_y_min, c2_y_max), (c2_z_min, c2_z_max) = cube
            if c2_x_max < c1_x_max:
                new_cubes.append(((c2_x_max + 1, c1_x_max), (c1_y_min, c1_y_max), (c1_z_min, c1_z_max)))
                c1_x_max = c2_x_max
            if c2_x_min > c1_x_min:
                new_cubes.append(((c1_x_min, c2_x_min - 1), (c1_y_min, c1_y_max), (c1_z_min, c1_z_max)))
                c1_x_min = c2_x_min
            if c2_y_max < c1_y_max:
                new_cubes.append(((c1_x_min, c1_x_max), (c2_y_max + 1, c1_y_max), (c1_z_min, c1_z_max)))
                c1_y_max = c2_y_max
            if c2_y_min > c1_y_min:
                new_cubes.append(((c1_x_min, c1_x_max), (c1_y_min, c2_y_min - 1), (c1_z_min, c1_z_max)))
                c1_y_min = c2_y_min
            if c2_z_max < c1_z_max:
                new_cubes.append(((c1_x_min, c1_x_max), (c1_y_min, c1_y_max), (c2_z_max + 1, c1_z_max)))
            if c2_z_min > c1_z_min:
                new_cubes.append(((c1_x_min, c1_x_max), (c1_y_min, c1_y_max), (c1_z_min, c2_z_min - 1)))
        if value:
            new_cubes.append(cube)
        cubes = new_cubes
    return cubes


def get_volume(cubes):
    volume = 0
    for (min_x, max_x), (min_y, max_y), (min_z, max_z) in cubes:
        volume += ((max_x - min_x + 1) * (max_y - min_y + 1) * (max_z - min_z + 1))
    return volume


def part_one_two():
    actions = format_data('input.txt')
    cubes = run_sequences_cube(actions[:20])
    print(get_volume(cubes))
    cubes = run_sequences_cube(actions)
    print(get_volume(cubes))


if __name__ == '__main__':
    part_one_two()
