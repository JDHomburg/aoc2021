from functions.data_in import read_data

open_bracket = {'<': '>', '[': ']', '(': ')', '{': '}'}
close_bracket = {')': 3, ']': 57, '}': 1197, '>': 25137}
missing_bracket = {'<': 4, '[': 2, '(': 1, '{': 3}


def check_line(line, corrupt=True):
    stack = list()
    for bracket in line:
        if bracket in open_bracket:
            stack.append(bracket)
        if bracket in close_bracket:
            if bracket == open_bracket[stack[-1]]:
                stack.pop(-1)
            else:
                if corrupt:
                    return close_bracket[bracket]
                else:
                    return 0
    if not corrupt and len(stack) > 0:
        result = 0
        for bracket in stack[::-1]:
            result = 5 * result + missing_bracket[bracket]
        return result
    return 0


def part_one():
    return sum([check_line(line) for line in read_data('input.txt')])


def part_two():
    scores = sorted([value for line in read_data('input.txt') if (value := check_line(line, corrupt=False)) > 0])
    return scores[len(scores) // 2]


print(part_one())
print(part_two())
