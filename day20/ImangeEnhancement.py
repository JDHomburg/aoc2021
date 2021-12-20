import numpy as np


def format_input(file_path='input.txt'):
    with open(file_path, 'r') as f:
        enhancement = (np.asarray(list(f.readline().strip())) == '#').astype(np.int32)
        f.readline()
        image = (np.asarray([list(line.strip()) for line in f.readlines()]) == '#').astype(np.int32)
    return enhancement, image


factors = np.asarray([[[2 ** i for i in range(9)][::-1]]])


def apply_enhancement(image, enhancement, ones=False):
    padding = 6
    padding_function = np.ones if ones else np.zeros
    padded_image = padding_function(tuple([shape + padding for shape in image.shape]))
    padded_image[padding // 2:-padding // 2, padding // 2:-padding // 2] = image
    enhanced_image_shape = tuple([shape + padding - 2 for shape in image.shape])
    idx_grid = get_idx_grid(enhanced_image_shape)
    bin_idx_map = padded_image[idx_grid[0], idx_grid[1]]
    idx_map = np.sum(bin_idx_map * factors, axis=-1).astype(np.int64)
    enhanced_image = enhancement[idx_map]
    return enhanced_image


x_area, y_area = np.meshgrid(np.arange(0, 3), np.arange(0, 3))
y_area, x_area = x_area.reshape(1, 1, -1), y_area.reshape(1, 1, -1)


def get_idx_grid(shape):
    x, y = np.arange(0, shape[0]), np.arange(0, shape[1])
    ys, xs = np.meshgrid(y, x)
    xs, ys = np.expand_dims(xs, axis=-1), np.expand_dims(ys, axis=-1)
    xs = xs + x_area
    ys = ys + y_area
    return xs, ys


def plot_image(image):
    for line in image:
        print(''.join('#' if v else '.' for v in line))


def enhance_n_times(image, enhancement, n, ones=False):
    ones = ones
    for _ in range(n):
        image = apply_enhancement(image, enhancement, ones=ones)
        ones = not ones
    return image, ones


def part_one_two():
    enhancement, input_image = format_input()
    image, _ = enhance_n_times(input_image, enhancement, 2)
    print(np.sum(image))
    image, _ = enhance_n_times(input_image, enhancement, 50)
    print(np.sum(image))


if __name__ == '__main__':
    part_one_two()
