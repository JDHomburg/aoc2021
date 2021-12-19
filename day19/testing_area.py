import numpy as np
from BeaconScanner import format_data, get_translation, get_transformations, transformation_generator


def test01():
    points = format_data('test_input.txt', beacons_per_scanner=6)
    points0 = points[0]

    translation = np.asarray([[0, 0, 10]])

    points0_ = points0 + translation

    points0 = np.concatenate([points0, points0[:3, :]])
    # points0 -> Nx3
    # points0_ -> Mx3
    # Nx3x1 - 1x3xM => Nx3xM
    # => points0 -> erweitern -> Nx3x1
    # => points0_ -> Achsen vertauschen -> 3xM -> erweitern -> 1x3xM
    difference_map = (np.expand_dims(points0, axis=2) - np.expand_dims(points0_.transpose((1, 0)), axis=0)).transpose(
        (0, 2, 1))

    difference_map_ = difference_map.reshape(-1, 3)
    # print(difference_map_.shape)
    # print(difference_map.shape)
    histogram, counts = np.unique(difference_map_, axis=0, return_counts=True)
    max_occurrence = np.max(counts)
    idx_max = np.where(counts == max_occurrence)
    max_vec = histogram[idx_max].reshape(-1)
    print(max_vec.shape, max_vec)
    idx_match = np.where((difference_map == max_vec).all(axis=2))
    print(idx_match)

    print(difference_map[idx_match[0], idx_match[1], :])

    # print(difference_map)
    # print(difference_map.shape)


def test02():
    points = format_data('test_input.txt', beacons_per_scanner=6)
    points0 = points[0]

    translation = np.asarray([[0, 0, 10]])

    points0_ = points0 + translation

    points0 = np.concatenate([points0, points0[:3, :]])

    print(get_translation(points0, points0_, min_matching=6))


def test03():
    # for v in transformation_generator():
    #     print(v)
    transforms = np.asarray([mat.tolist() for mat in transformation_generator()])
    print(transforms.shape)
    transforms_, counts = np.unique(transforms, return_counts=True, axis=0)
    print(len(transforms_))

    print('----------------------')
    for idx in np.where(counts > 1)[0]:
        print(transforms_[idx])
        print(np.where((transforms == transforms_[idx]).all(axis=1).all(axis=1)))


# test02()
test03()
