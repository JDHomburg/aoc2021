from functions.data_in import read_data
import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab

R_x = np.asarray([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
R_y = np.asarray([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
R_z = np.asarray([[0, -1, 0], [1, 0, 0], [0, 0, 1]])


def format_data(file_path='input.txt'):
    scanners = list()
    scanner = None
    for line in read_data(file_path):
        if line.startswith('---'):
            scanner = list()
        elif len(line) == 0:
            scanner_map = np.asarray(scanner)
            scanners.append(scanner_map)
        else:
            scanner.append(list(map(int, line.split(','))))
    scanner_map = np.asarray(scanner)
    scanners.append(scanner_map)
    return scanners


def get_diff_matrix(points_a, points_b):
    return np.expand_dims(points_a, axis=2) - np.expand_dims(points_b.transpose((1, 0)), axis=0)


def get_translation(points_a, points_b, min_matching=12):
    difference_map = get_diff_matrix(points_a, points_b)
    difference_map = difference_map.transpose((0, 2, 1))
    difference_map_ = difference_map.reshape(-1, 3)
    histogram, counts = np.unique(difference_map_, axis=0, return_counts=True)
    max_occurrence = np.max(counts)
    if max_occurrence < min_matching:
        return None, None
    idx_max = np.where(counts == max_occurrence)
    max_vec = histogram[idx_max].reshape(-1)
    idx_match = np.where((difference_map == max_vec).all(axis=2))
    unique_a = set(idx_match[0])
    unique_b = set(idx_match[1])
    if len(unique_a) < min_matching or len(unique_b) < min_matching:
        return None, None

    matching = dict()
    for a, b in zip(*idx_match):
        if a in unique_a and b in unique_b:
            matching[a] = b
            unique_a.remove(a)
            unique_b.remove(b)
    return max_vec, matching


def transformation_generator():
    axes = [
        np.asarray([1, 0, 0]),
        np.asarray([-1, 0, 0]),
        np.asarray([0, 1, 0]),
        np.asarray([0, -1, 0]),
        np.asarray([0, 0, 1]),
        np.asarray([0, 0, -1]),
    ]
    for idx1, axis1 in enumerate(axes):
        for idx2, axis2 in enumerate(axes):
            if idx1 == idx2:
                continue
            if np.all(axis1 == -axis2):
                continue
            axis3 = np.cross(axis1, axis2)
            yield np.stack([axis1, axis2, axis3])


def get_transformations(points):
    for mat in transformation_generator():
        yield np.matmul(points, mat)


def match_clouds(points):
    world = points[0]
    scanner_ids = list(range(1, len(points)))
    scanner_positions = [np.asarray([0, 0, 0])]

    plot_world = mlab.points3d(world[:, 0], world[:, 1], world[:, 2], scale_factor=0.001)
    mlab.show()
    while scanner_ids:
        matched = False
        for scanner_id in scanner_ids:
            for cloud in get_transformations(points[scanner_id]):
                translation, matching = get_translation(world, cloud)
                if translation is None:
                    continue
                matched = scanner_id, translation, matching, cloud
                break
            if matched:
                break
        if not matched:
            break
        scanner_id, translation, matching, cloud = matched
        scanner_ids.remove(scanner_id)
        cloud += translation
        scanner_positions.append(translation)
        print('Debug')
        mlab.clf()
        plot_world = mlab.points3d(world[:, 0], world[:, 1], world[:, 2], scale_factor=0.001)
        plot_scanner = mlab.points3d(cloud[:, 0], cloud[:, 1], cloud[:, 2], scale_factor=0.001)
        mlab.show()
        non_matching = set(range(cloud.shape[0])).difference(matching.values())
        world = np.concatenate([world, cloud[list(non_matching), :]], axis=0)
    return world, np.asarray(scanner_positions)


def part_one():
    scanner_maps = format_data()
    world, scanner_positions = match_clouds(scanner_maps)
    print(world.shape)
    diff_map = np.sum(get_diff_matrix(scanner_positions, scanner_positions), axis=1)
    print(np.max(diff_map))


if __name__ == '__main__':
    part_one()
