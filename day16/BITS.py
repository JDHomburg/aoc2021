from functions.data_in import read_data
import math


def format_data(file_path='input.txt'):
    data = read_data(file_path)
    result = hex_to_bin(data[0])
    return result


def hex_to_bin(hex_str):
    bits = len(hex_str) * 4
    return bin(int(hex_str, 16))[2:].zfill(bits)


def get_version_type(data):
    return int(data[:3], 2), data[3:]


def get_literal(data):
    number = ''
    for idx, part in enumerate(data[::5]):
        number += data[idx * 5 + 1:(idx + 1) * 5]
        if not bool(int(part)):
            break
    return int(number, 2), data[(idx + 1) * 5:]


def get_operator(data):
    if bool(int(data[0])):
        number = int(data[1:12], 2)
        return True, number, data[12:]
    else:
        bits = int(data[1:16], 2)
        data = data[16:]
        sub_packets = data[:bits]
        return False, sub_packets, data[bits:]


func_id_map = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda x: int(int(x[0]) > int(x[1])),  # greater than
    6: lambda x: int(int(x[0]) < int(x[1])),  # less than
    7: lambda x: int(int(x[0]) == int(x[1])),  # equal to
}


def process_packet(data):
    if len(data) < 8:
        return '', 0, []
    version_sum = 0
    version, data = get_version_type(data)
    version_sum += version
    type_id, data = get_version_type(data)
    if type_id == 4:
        literal, data = get_literal(data)
        return data, version_sum, literal
    else:
        is_number, number_data, data = get_operator(data)
        sub_values = list()
        if is_number:
            for _ in range(number_data):
                data, _version_sum, _values = process_packet(data)
                version_sum += _version_sum
                sub_values.append(_values)
        else:
            while number_data:
                number_data, _version_sum, _values = process_packet(number_data)
                version_sum += _version_sum
                sub_values.append(_values)
        return data, version_sum, func_id_map[type_id](sub_values)


def part_one_two():
    data = format_data()
    _, version_sum, values = process_packet(data)
    print('Part One', version_sum)
    print('Part Two', values)


if __name__ == '__main__':
    part_one_two()
