import numpy as np

from functions.data_in import read_data


def format_data():
    lines = read_data('input.txt')
    coordinates = [[int(value) for value in line.split(',')]
                   for line in lines if not line.startswith('fold') and len(line) > 0]
    folding = [o[2].split('=') for line in lines
               if line.startswith('fold') and len(line) > 0 and (o := line.split(' '))]

    shape = max([v[0] for v in coordinates]) + 1, max(v[1] for v in coordinates) + 1
    if shape[0] % 2 == 0:
        shape = (shape[0] + 1, shape[1])
    if shape[1] % 2 == 0:
        shape = (shape[0], shape[1] + 1)
    xs, ys = list(zip(*coordinates))
    coordinates = np.zeros(tuple(shape)).astype(np.bool_)
    coordinates[(np.asarray(xs).astype(np.int64), np.asarray(ys).astype(np.int64))] = True

    return coordinates.transpose((1, 0)), folding


def fold(paper, folding):
    axis, idx = folding
    idx = int(idx)
    if axis == 'x':
        return paper[:, :idx] | paper[:, :-(idx + 1):-1]
    else:
        return paper[:idx, :] | paper[:-(idx + 1):-1, :]


def print_paper(paper):
    for line in paper:
        print(''.join(['\u2588\u2588' if v else '  ' for v in line]).format('utf-8'))


def part_one():
    paper, foldings = format_data()
    paper = fold(paper, foldings[0])
    print(np.sum(paper))


def part_two():
    paper, foldings = format_data()
    for folding in foldings:
        paper = fold(paper, folding)

    print_paper(paper)


part_one()
part_two()
