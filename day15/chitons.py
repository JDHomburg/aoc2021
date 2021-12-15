import numpy as np
from bisect import insort


def format_data(file_name='input.txt'):
    with open(file_name, 'r') as f:
        result = np.asarray([[int(v) for v in line.strip()] for line in f.readlines()])
    return result


class SearchPos:
    def __init__(self, idx, risk, approx_risk, path):
        self.idx = idx
        self.risk = risk
        self.approx_risk = approx_risk
        self.path = path + [self.idx]
        self.value = self.risk + self.approx_risk

    def __lt__(self, other):
        if isinstance(other, SearchPos):
            return self.value < other.value


def a_star(map):
    max_x, max_y = map.shape
    target = (max_x - 1, max_y - 1)
    print(map.shape)

    def get_neighbors(idx):
        x, y = idx
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        if x < target[0]:
            yield x + 1, y
        if y < target[1]:
            yield x, y + 1

    def get_approx(idx):
        return 1.2 ** (max_x - idx[0]) + 1.2 ** (max_y - idx[1])

    start = (0, 0)
    stack = [SearchPos(start, map[start], sum(map.shape), [start])]
    while True:
        # print([pos.value for pos in stack])
        print(len(stack))
        pos = stack.pop(0)
        print(pos.idx, pos.value)
        if pos.idx == target:
            return pos
        for neighbor in get_neighbors(pos.idx):
            insort(stack, SearchPos(neighbor, pos.risk + map[neighbor], get_approx(neighbor), pos.path))
            # stack = stack[:100]


class Cell:
    def __init__(self, value, idx):
        self.idx = idx
        self.value = value
        self.path_value = np.inf
        self.prev = None
        self.neighbors = list()

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def update(self):
        changed = False
        for neighbor in self.neighbors:
            value = neighbor.path_value + self.value
            if value < self.path_value:
                self.prev = neighbor
                self.path_value = value
                changed = True
        return changed


def update_cell_neighbor(cell):
    return cell.update()


def add_neighbor(cell_a, cell_b):
    cell_a.add_neighbor(cell_b)


update_cell_neighbor = np.vectorize(update_cell_neighbor)
add_neighbor = np.vectorize(add_neighbor)


def bellman_ford(map):
    cells = np.asarray([[Cell(map[x, y], (x, y)) for x in range(map.shape[0])] for y in range(map.shape[1])])
    cells[0, 0].path_value = 0

    add_neighbor(cells[:-1, :], cells[1:, :])
    add_neighbor(cells[:, :-1], cells[:, 1:])
    add_neighbor(cells[1:, :], cells[:-1, :])
    add_neighbor(cells[:, 1:], cells[:, :-1])

    while np.any(update_cell_neighbor(cells)):
        pass
    return cells[-1, -1].path_value


def part_one(map):
    risk = bellman_ford(map)
    print(risk)


def extend_map(map):
    x_shape, y_shape = map.shape
    map = np.concatenate([map for _ in range(5)], axis=0)
    map = np.concatenate([map for _ in range(5)], axis=1)
    for x in range(5):
        for y in range(5):
            map[x * x_shape:(x + 1) * x_shape, y * y_shape:(y + 1) * y_shape] += (x + y)
    map = np.fmod(map - 1, 9) + 1
    return map


def part_two(map):
    map = extend_map(map)
    part_one(map)


part_one(format_data())
part_two(format_data())
