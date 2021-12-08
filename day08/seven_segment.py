from functions.data_in import read_data


def part_one():
    print(len([v for value in [(line.split('|')[1]).split() for line in read_data('input.txt')] for v in value
               if len(v) == 2 or len(v) == 3 or len(v) == 4 or len(v) == 7]))


part_one()

def get_number(code, key):
    code = ''.join(map(str, [key[''.join(sorted(c))] for c in code]))
    code = int(code)
    return code


def get_key(key):
    key_map = dict()
    sorted_by_length = dict()
    for v in key:
        sorted_by_length[len(v)] = sorted_by_length.get(len(v), list()) + [sorted(v)]
    one_string = ''.join(sorted_by_length[2][0])
    key_map[one_string] = 1
    seven_string = ''.join(sorted_by_length[3][0])
    key_map[seven_string] = 7
    four_string = ''.join(sorted_by_length[4][0])
    key_map[four_string] = 4
    eight_string = ''.join(sorted_by_length[7][0])
    key_map[eight_string] = 8

    for zero_six_nine in sorted_by_length[6]:
        if len(set(zero_six_nine).difference(one_string)) == 5:
            key_map[''.join(zero_six_nine)] = 6
        elif len(set(zero_six_nine).difference(four_string)) == 3:
            key_map[''.join(zero_six_nine)] = 0
        else:
            key_map[''.join(zero_six_nine)] = 9

    four_minus_one = set(four_string).difference(one_string)

    for two_three_five in sorted_by_length[5]:
        if len(set(two_three_five).difference(one_string)) == 3:
            key_map[''.join(two_three_five)] = 3
        elif len(set(two_three_five).difference(four_minus_one)) == 3:
            key_map[''.join(two_three_five)] = 5
        else:
            key_map[''.join(two_three_five)] = 2

    return key_map


def part_two():
    result = 0
    data = read_data('input.txt')
    # data = [' '.join(['abcefg', 'cf', 'acdeg', 'acdfg', 'acdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg'])+' | ']
    for line in data:
        key, code = line.split('|')
        result += get_number(code.split(), get_key(key.split()))
    print(result)


part_two()
