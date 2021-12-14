import numpy as np
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor


def format_data():
    with open('input.txt', 'r') as f:
        initial_poly = f.readline().strip()
        f.readline()
        rules = dict(line.strip().split(' -> ') for line in f.readlines())

    rules = {key: key[0] + value + key[1] for key, value in rules.items()}
    return initial_poly, rules


def n_th_step_rules(rules, n):
    tmp_rules = rules
    for i in range(n - 1):
        tmp_rules = {key: apply_rules(value, rules)
                     for key, value in tmp_rules.items()}
    return tmp_rules


def apply_rules(poly, rules):
    result = ''.join(rules[''.join(pair_)][:-1] for pair_ in zip(poly, poly[1:]))
    return result + poly[-1]


def func1(poly, rules, n):
    for _ in range(n):
        poly = apply_rules(poly, rules)
    return poly


def func2(poly, rules, n):
    rules = n_th_step_rules(rules, n)
    return apply_rules(poly, rules)

def debug1():
    for i in range(10):
        yield i

def debug2(gen):
    mem = None
    for obj in gen:
        if mem is None:
            mem = obj
            continue
        print(mem, obj)
        mem = obj


def part_one():
    initial_poly, rules = format_data()
    rules = n_th_step_rules(rules, 10)
    poly = apply_rules(initial_poly, rules)
    _, counts = np.unique(list(poly), return_counts=True)
    result = np.max(counts) - np.min(counts)
    return result


def test():
    initial_poly, rules = format_data()
    func1_time = list()
    func2_time = list()
    for n in range(2, 16):
        start = time.time()
        func1(initial_poly, rules, n)
        func1_time.append(time.time() - start)
        start = time.time()
        func2(initial_poly, rules, n)
        func2_time.append(time.time() - start)
    fig = plt.Figure()
    plt.plot(func1_time, label='func1')
    plt.plot(func2_time, label='func2')
    plt.legend()
    plt.show()


def part_one_():
    poly, rules = format_data()
    start = time.time()
    for i in range(40):
        poly = apply_rules(poly, rules)
    _, counts = np.unique(list(poly), return_counts=True)
    result = np.max(counts) - np.min(counts)
    print(time.time() - start)
    return result

    # initial_poly = 'NNCB'
    # print(apply_rules(initial_poly, rules))
    # print(initial_poly)
    # print(rules)


# print(part_one_())
# test()
debug2(debug1())