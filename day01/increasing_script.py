
def part_one():
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    increased = 0
    prev = None
    for line in lines:
        try:
            v = int(line)
            if prev is not None:
                increased += int(v > prev)
            prev = v
        except Exception:
            pass
    print(increased)

def part_two():
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    values = list()
    for line in lines:
        try:
            v = int(line)
            values.append(v)
        except Exception:
            pass

    running_sums = [values[i]+values[i+1]+values[i+2] for i in range(len(values)-2)]

    increased = 0
    prev = None
    for v in running_sums:
        if prev is not None:
            increased += int(v>prev)
        prev = v
    print(increased)

part_one()
part_two()