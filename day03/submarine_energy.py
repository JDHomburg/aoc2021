import numpy as np


def read_file():
    with open('input.txt', 'r') as f:
        values = [list(map(int, list(v.replace('\n', '')))) for v in f.readlines()]
    return values


def part_one():
    values = read_file()
    gamma_ = [1 if sum(bit) > len(values) / 2 else 0 for bit in zip(*values)]
    gamma = sum([bit * (2 ** exp) for exp, bit in enumerate(gamma_[::-1])])
    epsilon = sum([(1 - bit) * (2 ** exp) for exp, bit in enumerate(gamma_[::-1])])
    return epsilon * gamma


def part_two():
    values_ = np.asarray(read_file())
    oxygen_gen = values_.copy()
    co2_scrub = values_
    for idx in range(oxygen_gen.shape[1]):
        target = 1 if np.sum(oxygen_gen, axis=0)[idx] >= oxygen_gen.shape[0]/2 else 0
        mask = np.where(oxygen_gen[:, idx] == target)
        oxygen_gen = oxygen_gen[mask]

        if co2_scrub.shape[0]>1:
            target = 1 if np.sum(co2_scrub, axis=0)[idx] < co2_scrub.shape[0]/2 else 0
            mask = np.where(co2_scrub[:, idx] == target)
            co2_scrub = co2_scrub[mask]

    factor = np.asarray([[2**i] for i in range(co2_scrub.shape[1])[::-1]])
    return int(np.matmul(co2_scrub,factor)*np.matmul(oxygen_gen,factor))


print(part_one())
print(part_two())
