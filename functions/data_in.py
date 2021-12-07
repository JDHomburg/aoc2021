def read_data(file_path):
    with open(file_path, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data