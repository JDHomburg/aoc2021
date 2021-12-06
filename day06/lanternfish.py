def read_data():
    with open('input.txt', 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


def one_day(population):
    result = {**{i - 1: population.get(i, 0) for i in range(1, 9)}, **{8: population.get(0, 0)}}
    result[6] += population.get(0, 0)
    return result


def n_days(n):
    population = [int(state) for line in read_data() for state in line.split(',')]
    population = np.unique(population, return_counts=True)
    population = {key: value for key, value in zip(*population)}

    for _ in range(n):
        population = one_day(population)
    return sum(population.values())


def part_one():
    return n_days(80)


def part_two():
    return n_days(256)


print(part_one())
print(part_two())
