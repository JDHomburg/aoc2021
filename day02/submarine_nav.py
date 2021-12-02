def read_file():
    value_map = {'forward': (0, 1), 'down': (1, 1), 'up': (1, -1)}
    with open('input.txt', 'r') as f:
        navigation = [(value_map[v[0]][0], value_map[v[0]][1] * int(v[1])) for v in
                      [nav.split(' ') for nav in f.readlines() if len(nav) > 1]]
    return navigation


def part_one():
    start = [0, 0]
    for nav in read_file():
        start[nav[0]] += nav[1]
    return start[0] * start[1]


def part_two():
    start = [0, 0]
    aim = 0
    for nav in read_file():
        if not bool(nav[0]):
            start[0] += nav[1]
            start[1] += aim * nav[1]
        else:
            aim += nav[1]
    return start[0] * start[1]


print(part_one())
print(part_two())
