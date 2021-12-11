from functions.data_in import read_data
import numpy as np


def format_data():
    return np.asarray([[int(v) for v in line] for line in read_data('input.txt')])


lateral_area = np.asarray([[-1, -1], [-1, 0], [0, -1], [-1, 1], [1, -1], [0, 1], [1, 0], [1, 1]]).reshape((8, 2, 1))


def get_flash_addition(idxs):
    idxs = np.asarray(idxs)
    lateral = (lateral_area + idxs).transpose((0, 2, 1))
    mask = np.sum((lateral < 0) | (lateral >= 10), axis=2)
    lateral = lateral[np.where(mask == 0)].astype(np.int64)
    lateral = (lateral[:, 0], lateral[:, 1], np.linspace(0, lateral.shape[0] - 1, lateral.shape[0]).astype(np.int64))
    addition = np.zeros((10, 10, lateral[0].shape[0]))
    addition[lateral] = 1
    return np.sum(addition, axis=2).astype(np.int32)


def update_energy(energy_levels):
    do = True
    to_flash = total_flash = np.zeros((10, 10)).astype(np.bool_)
    energy_levels += 1
    while do or np.sum(to_flash):
        do = False
        to_flash = (energy_levels > 9) & (~total_flash)
        total_flash = total_flash | to_flash
        addition = get_flash_addition(np.where(to_flash))
        energy_levels += addition
    energy_levels[np.where(energy_levels > 9)] = 0
    return energy_levels, np.sum(total_flash)


def part_one():
    energy_levels = format_data()
    total_flashes = 0
    for _ in range(100):
        energy_levels, flashes = update_energy(energy_levels)
        total_flashes += flashes
    print(total_flashes)


def part_two():
    energy_levels = format_data()
    flashes = 0
    idx = 0
    while flashes != 100:
        energy_levels, flashes = update_energy(energy_levels)
        idx += 1
    print(idx)


part_one()
part_two()
