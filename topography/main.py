import random
import math
from typing import List, Tuple


def find_local_min(matrix: List[List[int]], i: int, j: int) -> List[Tuple[Tuple[int, int], float, float]]:
    def get_neighbors(i: int, j: int) -> List[Tuple[int, int]]:
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [(x, y) for x, y in neighbors if 0 <= x < len(matrix) and 0 <= y < len(matrix[0])]

    path = [((i, j), 0, 0)]
    while True:
        neighbors = get_neighbors(i, j)
        differences = [(x, y, matrix[i][j] - matrix[x][y])
                       for x, y in neighbors]
        largest_diff = max(differences, key=lambda x: x[2])

        if largest_diff[2] <= 0:
            break

        i, j, diff = largest_diff
        hypotenuse = math.sqrt(diff ** 2 + 1 ** 2)
        angle = math.degrees(math.atan(diff))
        path.append(((i, j), hypotenuse, angle))

    return path


def print_path_on_matrix(matrix: List[List[int]], path: List[Tuple[Tuple[int, int], float, float]]):
    path_coords = {coord for coord, _, _ in path}

    for i, row in enumerate(matrix):
        row_str = []
        for j, value in enumerate(row):
            if (i, j) in path_coords:
                row_str.append("X")
            else:
                row_str.append(str(value))
        print(" ".join(row_str))


if __name__ == "__main__":

    matrix = [
        [0,  0,  3,  6,  6,  6,  6,  3,  0,  0],
        [0,  3,  8, 9, 9, 9, 9,  8,  3,  0],
        [3,  8,  5,  2,  1,  1,  2,  5,  8,  3],
        [6, 9,  2,  0,  0,  0,  0,  2, 9,  6],
        [6, 9,  1,  0,  0,  0,  0,  1, 9,  6],
        [6, 9,  1,  0,  0,  0,  0,  1, 9,  6],
        [6, 9,  2,  0,  0,  0,  0,  2, 9,  6],
        [3,  8,  5,  2,  1,  1,  2,  5,  8,  3],
        [0,  3,  8, 9, 9, 9, 9,  8,  3,  0],
        [0,  0,  3,  6,  6,  6,  6,  3,  0,  0]
    ]
    starting_i, starting_j = 3, 1
    path = find_local_min(matrix, starting_i, starting_j)
    print_path_on_matrix(matrix, path)
