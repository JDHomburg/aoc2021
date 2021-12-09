from functions.data_in import read_data
import numpy as np


def format_data():
    data = np.asarray([[int(v) for v in line] for line in read_data('input.txt')])
    data_padded = data.copy()
    nines = np.ones((1, data_padded.shape[1])) * 9
    data_padded = np.concatenate([nines, data_padded, nines], axis=0)
    nines = np.ones((data_padded.shape[0], 1)) * 9
    data_padded = np.concatenate([nines, data_padded, nines], axis=1)
    return data, data_padded


def get_min_idx(data_padded):
    rolled1 = np.roll(data_padded, 1, axis=1)
    rolled2 = np.roll(data_padded, -1, axis=1)
    rolled3 = np.roll(data_padded, 1, axis=0)
    rolled4 = np.roll(data_padded, -1, axis=0)
    idx = np.where((data_padded < rolled1) & (data_padded < rolled2) &
                   (data_padded < rolled3) & (data_padded < rolled4))
    return idx


def part_one():
    data, data_padded = format_data()
    idx = get_min_idx(data_padded)
    return np.sum(data_padded[idx] + 1)


def get_neighbor(idx, maxv):
    max_x, max_y = maxv
    if idx[0] - 1 >= 0:
        yield idx[0] - 1, idx[1]
    if idx[0] + 1 < max_x:
        yield idx[0] + 1, idx[1]
    if idx[1] - 1 >= 0:
        yield idx[0], idx[1] - 1
    if idx[1] + 1 < max_y:
        yield idx[0], idx[1] + 1


class Bassin:
    def __init__(self, idx, map):
        self.idx = idx
        self.value = map[idx]
        self.border = [(idx, self.value)]
        self.counter = 1
        self.viewed = {self.idx}

    def update(self, map):
        new_border = list()
        updated = False
        for _idx, value in self.border:
            for neighbor in get_neighbor(_idx, map.shape):
                if map[neighbor] > value:
                    updated = True
                    new_border.append((neighbor, map[neighbor]))
                    if neighbor not in self.viewed and map[neighbor] < 9:
                        self.counter += 1
                        self.viewed.add(neighbor)
        self.border = new_border
        return updated


def part_two():
    data, data_padded = format_data()
    idxX, idxY = get_min_idx(data_padded)
    bassins = [Bassin((x, y), data) for x, y in zip(idxX - 1, idxY - 1)]
    while any([bassin.update(data) for bassin in bassins]):
        continue
    result = 1
    for bassin in sorted(bassins, key=lambda x: x.counter, reverse=True)[:3]:
        result *= bassin.counter
    return result


print(part_one())
print(part_two())
