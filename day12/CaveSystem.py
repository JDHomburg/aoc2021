from functions.data_in import read_data
import numpy as np


class CaveGraph:
    class Node:
        def __init__(self, name):
            self.name = name
            self._neighbors = set()

        def __copy__(self):
            result = object.__new__(CaveGraph.Node)
            result.name = str(self.name)
            result._neighbors = {v.__copy__() for v in self._neighbors}
            return result

        def __iadd__(self, other):
            if isinstance(other, CaveGraph.Node):
                self._neighbors.add(other)
            return self

        def __eq__(self, other):
            if isinstance(other, CaveGraph.Node) and other.name == self.name:
                return True
            return False

        def __lt__(self, other):
            if isinstance(other, CaveGraph.Node):
                return self.name.__lt__(other.name)
            return False

        def __hash__(self):
            return hash(self.name)

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name

        @property
        def neighbors(self):
            return self._neighbors

    class BigCave(Node):
        pass

    class SmallCave(Node):
        pass

    def __init__(self):
        self.nodes = dict()

    def add_edge(self, _from: str, _to: str):
        _from_node = self.nodes.get(_from, None)
        if _from_node is None:
            if _from.isupper():
                _from_node = CaveGraph.BigCave(_from)
            else:
                _from_node = CaveGraph.SmallCave(_from)
            self.nodes[_from] = _from_node

        _to_node = self.nodes.get(_to, None)
        if _to_node is None:
            if _to.isupper():
                _to_node = CaveGraph.BigCave(_to)
            else:
                _to_node = CaveGraph.SmallCave(_to)
            self.nodes[_to] = _to_node

        _from_node += _to_node
        _to_node += _from_node

    def get_all_paths(self, _from: str, _to: str, small_cave_single: bool = True):
        _from = self.nodes[_from]
        _to = self.nodes[_to]
        stack = [(_from, [_from])]
        paths = set()

        while stack:
            node, visited = stack.pop()
            for neighbor in node.neighbors:
                if isinstance(neighbor, CaveGraph.SmallCave) and neighbor in visited:
                    if small_cave_single:
                        continue
                    else:
                        if neighbor == _from:
                            continue
                        small_caves = np.unique([v for v in visited if isinstance(v, CaveGraph.SmallCave)],
                                                return_counts=True)[1]
                        one_visited_twice = np.sum(small_caves > 1)
                        if one_visited_twice:
                            continue
                if neighbor == _to:
                    paths.add(tuple(visited) + (neighbor,))
                    continue
                stack.append((neighbor, list(visited) + [neighbor]))
        return paths


graph = CaveGraph()
for line in read_data('input.txt'):
    line = line.split('-')
    graph.add_edge(line[0], line[1])


def part_one():
    paths = graph.get_all_paths('start', 'end')
    print(len(paths))


def part_two():
    paths = graph.get_all_paths('start', 'end', small_cave_single=False)
    print(len(paths))


part_one()
part_two()
