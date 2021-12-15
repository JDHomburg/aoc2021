import numpy as np
import time
import matplotlib.pyplot as plt
from multiprocessing import Pool


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


def apply_parallel(args):
    stack_item, counts, rules, n = args
    stack = [stack_item]
    while stack:
        pair, k = stack.pop(-1)
        if k >= n:
            continue
        repl = rules[pair]
        counts[repl[1]] += 1
        stack.append((repl[:-1], k + 1))
        stack.append((repl[1:], k + 1))
    return counts


def apply_rules_n_times_and_count(poly, rules, n):
    counts = {v[1]: 0 for v in rules.values()}
    stack = [((''.join(pair), 0), counts.copy(), rules, n) for pair in zip(poly, poly[1:])]
    pool = Pool(16)
    count_list = pool.map(apply_parallel, stack)
    for counts_ in count_list:
        for key in counts_.keys():
            counts[key] += counts_[key]
    for p in poly:
        counts[p] += 1
    return counts


def dict_hack(poly, rules, n):
    pair_dict = dict()
    for pair in zip(poly, poly[1:]):
        key = ''.join(pair)
        pair_dict[key] = pair_dict.get(key, 0) + 1

    for _ in range(n):
        new_pair_dict = dict()
        for pair, count in pair_dict.items():
            a, b, c = rules[pair]
            new_pair_dict[a+b] = new_pair_dict.get(a+b, 0) + count
            new_pair_dict[b+c] = new_pair_dict.get(b+c, 0) + count
        pair_dict = new_pair_dict

    counts = dict()
    for (a,b), count in pair_dict.items():
        counts[a] = counts.get(a, 0) + count
        counts[b] = counts.get(b, 0) + count

    return counts


def func1(poly, rules, n):
    for _ in range(n):
        poly = apply_rules(poly, rules)
    _, counts = np.unique(list(poly), return_counts=True)
    result = np.max(counts) - np.min(counts)
    return result


def func2(poly, rules, n):
    rules = n_th_step_rules(rules, n)
    poly = apply_rules(poly, rules)
    _, counts = np.unique(list(poly), return_counts=True)
    result = np.max(counts) - np.min(counts)
    return result


def part_one():
    initial_poly, rules = format_data()
    rules = n_th_step_rules(rules, 10)
    poly = apply_rules(initial_poly, rules)
    _, counts = np.unique(list(poly), return_counts=True)
    result = np.max(counts) - np.min(counts)
    return result


def test():
    initial_poly, rules = format_data()
    naive_time = list()
    precompute_rules_time = list()
    multiprocess_time = list()
    dict_hack_time = list()

    for n in range(2, 20):
        start = time.time()
        func1(initial_poly, rules, n)
        naive_time.append(time.time() - start)
        start = time.time()
        func2(initial_poly, rules, n)
        precompute_rules_time.append(time.time() - start)
        start = time.time()
        counts = apply_rules_n_times_and_count(initial_poly, rules, n)
        result = max(counts.values())-min(counts.values())
        multiprocess_time.append(time.time() - start)
        start = time.time()
        counts = dict_hack(initial_poly, rules, n)
        result = (max(counts.values()) - min(counts.values()))//2+1
        dict_hack_time.append(time.time()-start)

    fig = plt.Figure()
    plt.plot(naive_time, label='naive')
    plt.plot(precompute_rules_time, label='precompute rules')
    plt.plot(multiprocess_time, label='multiprocess')
    plt.plot(dict_hack_time, label='dict hack')
    plt.legend()
    plt.show()


def part_two():
    poly, rules = format_data()
    counts = dict_hack(poly, rules, 40)
    return (max(counts.values()) - min(counts.values()))//2+1


if __name__ == '__main__':
    print(part_one())
    print(part_two())
    # test()
