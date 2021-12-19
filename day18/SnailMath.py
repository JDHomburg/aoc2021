from functions.data_in import read_data
import math


class SnailPair:
    def __init__(self, left, right):
        if isinstance(left, list):
            self.left = SnailPair(*left)
        else:
            self.left = left
        if isinstance(right, list):
            self.right = SnailPair(*right)
        else:
            self.right = right

    def reduce(self, max_iterations=None):
        iteration_count = 0
        while True:
            iteration_count += 1
            if self.__explode():
                if max_iterations is None or iteration_count <= max_iterations:
                    continue
            if self.__split():
                if max_iterations is None or iteration_count <= max_iterations:
                    continue
            break

    def __explode(self, depth=0):
        if isinstance(self.left, SnailPair):
            explosion_debris = self.left.__explode(depth=depth + 1)
            if isinstance(explosion_debris, tuple):
                if depth == 3:
                    self.left = 0
                if explosion_debris[1] is not None:
                    if isinstance(self.right, SnailPair):
                        self.right._add_to_left_most(explosion_debris[1])
                    else:
                        self.right += explosion_debris[1]
                if explosion_debris[0] is not None and depth > 0:
                    return explosion_debris[0], None
                return True
            elif explosion_debris:
                return True

        if isinstance(self.right, SnailPair):
            explosion_debris = self.right.__explode(depth=depth + 1)
            if isinstance(explosion_debris, tuple):
                if depth == 3:
                    self.right = 0
                if explosion_debris[0] is not None:
                    if isinstance(self.left, SnailPair):
                        self.left._add_to_right_most(explosion_debris[0])
                    else:
                        self.left += explosion_debris[0]
                if explosion_debris[1] is not None and depth > 0:
                    return None, explosion_debris[1]
                return True
            elif explosion_debris:
                return True

        if depth > 3:
            return self.left, self.right
        return False

    def _add_to_left_most(self, value):
        if isinstance(self.left, SnailPair):
            self.left._add_to_left_most(value)
        else:
            self.left += value

    def _add_to_right_most(self, value):
        if isinstance(self.right, SnailPair):
            self.right._add_to_right_most(value)
        else:
            self.right += value

    def __split(self):
        if isinstance(self.left, SnailPair):
            if self.left.__split():
                return True
        else:
            if self.left > 9:
                self.left = SnailPair(math.floor(self.left / 2), math.ceil(self.left / 2))
                return True
        if isinstance(self.right, SnailPair):
            if self.right.__split():
                return True
        else:
            if self.right > 9:
                self.right = SnailPair(math.floor(self.right / 2), math.ceil(self.right / 2))
                return True
        return False

    def __add__(self, other):
        if isinstance(other, SnailPair):
            result = SnailPair(self.__copy__(), other.__copy__())
            result.reduce()
            return result
        return None

    def __int__(self):
        return 3 * int(self.left) + 2 * int(self.right)

    def __str__(self):
        return '[' + str(self.left) + ',' + str(self.right) + ']'

    def __copy__(self):
        return SnailPair(self.left.__copy__() if isinstance(self.left, SnailPair) else self.left,
                         self.right.__copy__() if isinstance(self.right, SnailPair) else self.right)


def format_line(line, context):
    current_number = ''
    while line:
        if line[0] == '[':
            sub_list, line = format_line(line[1:], list())
            context.append(sub_list)
        elif line[0] == ']':
            if current_number:
                context.append(int(current_number))
            return context, line[1:]
        elif line[0] == ',':
            if current_number:
                context.append(int(current_number))
                current_number = ''
            line = line[1:]
        else:
            current_number += line[0]
            line = line[1:]

    return context[0]


def format_data(file_path='input.txt'):
    lines = list()
    for line in read_data(file_path):
        lines.append(format_line(line, list()))
    return lines


def test_reduction(input_, expectation_):
    number = SnailPair(*format_line(input_, []))
    number.reduce(max_iterations=0)
    print('Passed' if str(number) == expectation_ else (input_, str(number), expectation_))


def test_addition(input_a, input_b, expectation_):
    number_a = SnailPair(*format_line(input_a, []))
    number_b = SnailPair(*format_line(input_b, []))
    number = number_a + number_b
    print('Passed' if str(number) == expectation_ else (str(number), expectation_))


def test_magnitude(input_, expectation_):
    number_ = SnailPair(*format_line(input_, []))
    value = int(number_)
    print('Passed' if value == expectation_ else (value, expectation_))


def test_sum(input_, expected_sum, expected_magnitude):
    number = SnailPair(*format_line(input_[0], []))
    for line in input_[1:]:
        to_add = SnailPair(*format_line(line, []))
        number_ = number + to_add
        number_.reduce()
        print('   ', str(number))
        print(' + ', str(to_add))
        print(' = ', str(number_), '\n')
        number = number_
    print('Passed' if str(number) == expected_sum else (str(number), expected_sum))
    print('Passed' if int(number) == expected_magnitude else (int(number), expected_magnitude))


def test():
    test_reduction('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
    test_reduction('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
    test_reduction('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
    test_reduction('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    test_reduction('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

    test_addition('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

    test_magnitude('[[1,2],[[3,4],5]]', 143)
    test_magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384)
    test_magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445)
    test_magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791)
    test_magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137)
    test_magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488)

    test_sum(['[1,1]', '[2,2]', '[3,3]', '[4,4]'], '[[[[1,1],[2,2]],[3,3]],[4,4]]', 445)
    test_sum(['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]'], '[[[[3,0],[5,3]],[4,4]],[5,5]]', 791)
    test_sum(['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]'], '[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137)

    test_sum([
        '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
        '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
        '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
        '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
        '[7,[5,[[3,8],[1,4]]]]',
        '[[2,[2,2]],[8,[8,1]]]',
        '[2,9]',
        '[1,[[[9,3],9],[[9,0],[0,7]]]]',
        '[[[5,[7,4]],7],1]',
        '[[[[4,2],2],6],[8,7]]'],
        '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488)

    test_sum(['[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
              '[[[5,[2,8]],4],[5,[[9,9],0]]]',
              '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
              '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
              '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
              '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
              '[[[[5,4],[7,7]],8],[[8,3],8]]',
              '[[9,3],[[9,9],[6,[4,9]]]]',
              '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
              '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'],
             '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]',
             4140)


def part_one():
    data = format_data()
    value = SnailPair(*data[0])
    for line in data[1:]:
        value += SnailPair(*line)
    print(int(value))


def part_two():
    data = [SnailPair(*line) for line in format_data()]
    max_magnitude = 0
    for idx, number_a in enumerate(data):
        for number_b in data[idx + 1:]:
            max_magnitude = max(max_magnitude, int(number_a + number_b))
    print(max_magnitude)


if __name__ == '__main__':
    # test()
    part_one()
    part_two()
