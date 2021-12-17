from functions.data_in import read_data
import math


def get_target_area(file_path='input.txt'):
    _, data = read_data(file_path)[0].split('x=')
    xmin, data, ymax = data.split('..')
    xmax, ymin = data.split(', y=')
    return (int(xmin), int(xmax)), (int(ymin), int(ymax))


def get_x_speed(minx, maxx):
    # x + (x-1) + (x-2) ... + 0 = sum_i=1^x = x*(x+1)/2
    # minx <= x*(x+1)/2) <= maxx
    # minx = x*(x+1)/2 => x^2+x-2minx = 0
    x_speed = math.ceil(-0.5 + ((-0.5) ** 2 + minx * 2) ** 0.5)
    final_x = x_speed * (x_speed + 1) / 2
    assert minx <= final_x <= maxx
    return x_speed


def get_y_speed(miny, maxy):
    # y + y-1 + y-2 + y-3 + ...
    # k*y + sum_i=0^(k-1)[-i] = k*y - (k-1)*k/2
    y_speed = miny - 1
    last_y_speed = list()
    last_update = 0
    while True:
        last_update += 1
        y_speed += 1
        p_2 = (2 * y_speed + 1) / 2
        k = math.floor(p_2 + math.sqrt(p_2 ** 2 - 2 * miny))
        y_target = k * y_speed - k * (k - 1) / 2
        if miny <= y_target <= maxy:
            last_y_speed.append(y_speed)
            print('Y speed', y_speed)
            last_update = 0
        if last_update > 100:
            break
    return last_y_speed


def get_y_speed2(x_speed, minx, maxx, miny, maxy):
    y_speed = 0
    last_y_speed = y_speed
    last_update = 0
    while True:
        y_speed += 1
        last_update += 1
        trajectory = get_trajectory(x_speed, y_speed, minx, maxx, miny, maxy)
        if miny <= trajectory[-1][1] <= maxy:
            last_y_speed = y_speed
            last_update = 0
            print(max([p[1] for p in trajectory]))

        if last_update > 100:
            break
    return last_y_speed


def get_trajectory(x_speed, y_speed, xmin, xmax, ymin, ymax):
    trajectory = [(0, 0)]
    while not (xmin <= trajectory[-1][0] <= xmax and ymin <= trajectory[-1][1] <= ymax):
        x, y = trajectory[-1]
        x += x_speed
        if x_speed > 0:
            x_speed -= 1
        y += y_speed
        y_speed -= 1
        trajectory.append((x, y))
        if y < ymin or x > xmax:
            return []
    return trajectory


def get_all_speeds(minx, maxx, miny, maxy):
    speeds = list()
    for x_speed in range(maxx + 1):
        for y_speed in range(miny, 200):
            if get_trajectory(x_speed, y_speed, minx, maxx, miny, maxy):
                speeds.append((x_speed, y_speed))
    return speeds


def get_x_y_speed(minx, maxx, miny, maxy):
    x_speed = math.ceil(-0.5 + ((-0.5) ** 2 + minx * 2) ** 0.5)

    y_speed = miny - 1
    speeds = list()
    last_update = 0
    while True:
        last_update += 1
        y_speed += 1
        p_2 = (2 * y_speed + 1) / 2
        n = math.floor(p_2 + math.sqrt(p_2 ** 2 - 2 * miny))
        y_target = n * y_speed - n * (n - 1) / 2
        if miny <= y_target <= maxy:
            if n >= x_speed - 1:
                speeds.append((x_speed, y_speed))
                if (n != 1):
                    x_speed_ = math.ceil((2 * minx + n + n ** 2) / (2 - 2 * n))
                    speeds.append((x_speed_, y_speed))
                pass
            print(n, y_speed, y_target)
            last_update = 0
        if last_update > 100:
            break
    return speeds


def part_one():
    xrange, yrange = get_target_area()
    x_speed = get_x_speed(*xrange)
    y_speed = get_y_speed(*yrange)[-1]
    trajectory = get_trajectory(x_speed, y_speed, *xrange, *yrange)
    print(max([p[1] for p in trajectory]))


def part_two():
    # xrange, yrange = get_target_area('testinput.txt')
    xrange, yrange = get_target_area()

    # x_y_speed = get_x_y_speed(*xrange, *yrange)
    # print(x_y_speed)
    # print(len(x_y_speed))
    print(len(get_all_speeds(*xrange, *yrange)))


if __name__ == '__main__':
    # part_one()
    part_two()
