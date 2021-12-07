import numpy as np
from functions.data_in import read_data


def format_data():
    return np.asarray([int(v) for line in read_data('input.txt') for v in line.split(',')])


def get_fuel_linear(position, target):
    return np.sum(np.abs(position - target))


def get_fuel_incremental(position, target):
    diff = np.abs(position - target)
    return np.sum(diff * (diff + 1) / 2)


def part_one():
    data = format_data()
    target_position = min(list(range(0, np.max(data))), key=lambda x: get_fuel_linear(data, x))
    return target_position, get_fuel_linear(data, target_position)


def part_two():
    data = format_data()
    target_position = min(list(range(0, np.max(data))), key=lambda x: get_fuel_incremental(data, x))
    return target_position, get_fuel_incremental(data, target_position)


print(part_one()[1])
print(part_two()[1])
