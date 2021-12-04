import numpy as np


def read_input():
    with open('input.txt', 'r') as f:
        input = [line.replace('\n', '') for line in f.readlines()]
    drawn_numbers = list(map(int, input[0].split(',')))
    boards = np.asarray(
        [[list(map(int, [row[j * 3:j * 3 + 2] for j in range(5)])) for row in input[i * 6 + 2:(i + 1) * 6 + 1]]
         for i in range(len(input) // 6)])
    return drawn_numbers, boards


def part_one():
    drawn_numbers, boards = read_input()
    masks = np.zeros(boards.shape)
    mask, board, number = None, None, None

    for number in drawn_numbers:
        masks[np.where(boards == number)] = 1
        vert = np.sum(masks, axis=1)
        horz = np.sum(masks, axis=2)
        idx_vert = np.where(vert == 5)
        if idx_vert[0].size > 0:
            board = boards[idx_vert[0], :, :]
            mask = masks[idx_vert[0], :, :]
            break
        idx_horz = np.where(horz == 5)
        if idx_horz[0].size > 0:
            board = boards[idx_horz[0], :, :]
            mask = masks[idx_vert[0], :, :]
            break
    board[np.where(mask == 1)] = 0
    return np.sum(board) * number


def part_two():
    drawn_numbers, boards = read_input()
    masks = np.zeros(boards.shape)
    boards_count = masks.shape[0]
    mask, board, loosing_board, number = None, None, None, None

    for number in drawn_numbers:
        masks[np.where(boards == number)] = 1
        vert = np.sum(masks, axis=1)
        horz = np.sum(masks, axis=2)
        idx_vert = np.where(vert == 5)[0]
        idx_horz = np.where(horz == 5)[0]
        winning_boards = set(idx_vert).union(set(idx_horz))
        if len(winning_boards) == boards_count - 1:
            loosing_board = boards_count * (boards_count - 1) // 2 - sum(winning_boards)
        if len(winning_boards) == boards_count:
            board = boards[loosing_board, :, :]
            mask = masks[loosing_board, :, :]
            break

    board[np.where(mask == 1)] = 0
    return np.sum(board) * number


print(part_one())
print(part_two())
