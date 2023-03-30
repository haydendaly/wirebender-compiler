import random
import math
from typing import List, Tuple
import numpy as np
from noise import pnoise2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.ndimage import zoom

from matrix import imgToPrunedMatrix

def generate_mountain_range(size: int, scale: float = 0.05, octaves: int = 2, persistence: float = 2, lacunarity: float = 0.5):
    mountain_range = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            mountain_range[i, j] = pnoise2(i * scale, j * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=size, repeaty=size)
    mountain_range = (mountain_range - mountain_range.min()) / (mountain_range.max() - mountain_range.min())
    return mountain_range * 10

def find_local_min(mountain_range: np.ndarray) -> list:
    height, width = mountain_range.shape
    max_index = np.unravel_index(np.argmax(mountain_range), mountain_range.shape)
    i, j = max_index
    path = [((i, j), 0, 0)]

    def neighbors(i, j):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                ni, nj = i + x, j + y
                if 0 <= ni < height and 0 <= nj < width:
                    yield ni, nj

    while True:
        min_neighbor = None
        min_height = mountain_range[i, j]
        current_height = min_height

        for ni, nj in neighbors(i, j):
            neighbor_height = mountain_range[ni, nj]
            if neighbor_height < min_height:
                min_height = neighbor_height
                min_neighbor = (ni, nj)

        if min_neighbor is None:
            break

        ni, nj = min_neighbor
        if mountain_range[ni, nj] >= current_height:
            break

        height_diff = current_height - min_height
        hypotenuse = np.sqrt(height_diff ** 2 + 1)
        angle = np.degrees(np.arcsin(height_diff / hypotenuse))
        path.append(((ni, nj), hypotenuse, angle))
        i, j = ni, nj

    return path

def find_local_min_sgd(mountain_range: np.ndarray, learning_rate: float = 0.1, num_iterations: int = 1000) -> list:
    height, width = mountain_range.shape
    max_index = np.unravel_index(np.argmax(mountain_range), mountain_range.shape)
    i, j = max_index
    path = [((i, j), 0, 0)]

    def gradient(i, j):
        di, dj = 0, 0
        if i > 0:
            di += mountain_range[i, j] - mountain_range[i - 1, j]
        if i < height - 1:
            di -= mountain_range[i + 1, j] - mountain_range[i, j]
        if j > 0:
            dj += mountain_range[i, j] - mountain_range[i, j - 1]
        if j < width - 1:
            dj -= mountain_range[i, j + 1] - mountain_range[i, j]
        return di, dj

    for _ in range(num_iterations):
        di, dj = gradient(i, j)
        i = np.clip(i - int(learning_rate * di), 0, height - 1)
        j = np.clip(j - int(learning_rate * dj), 0, width - 1)
        current_height = mountain_range[i, j]
        path.append(((i, j), 0, 0))

    return path

def local_min_to_wirebender(local_min_path: list, unit_length: float = 1.0) -> str:
    wirebender_commands = []

    for i in range(len(local_min_path) - 1):
        (x1, y1), z_diff1 = local_min_path[i]
        (x2, y2), z_diff2 = local_min_path[i + 1]
        dx, dy = (x2 - x1) * unit_length, (y2 - y1) * unit_length
        dz = (z_diff2 - z_diff1) * unit_length
        feed_distance = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        wirebender_commands.append(f"feed {feed_distance:.2f}")

        if i < len(local_min_path) - 2:
            (x3, y3), z_diff3 = local_min_path[i + 2]
            angle_xy = np.degrees(np.arctan2(y3 - y2, x3 - x2))
            angle_z = np.degrees(np.arctan2(z_diff3 - z_diff2, np.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)))
            wirebender_commands.append(f"bend {angle_xy:.2f}")
            wirebender_commands.append(f"rotate {angle_z:.2f}")

    return "\n".join(wirebender_commands)


def plot_topography_3d(mountain_range: np.ndarray, local_min_path: list = None):
    height, width = mountain_range.shape
    X, Y = np.meshgrid(np.arange(0, width), np.arange(0, height))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, mountain_range, cmap="terrain", alpha=0.7)
    if local_min_path:
        x_coords, y_coords, z_coords = zip(*[(x, y, mountain_range[x, y] + 2) for (x, y), _, _ in local_min_path])
        ax.plot(y_coords, x_coords, z_coords, marker='o', markersize=5, linestyle='-', color='red', linewidth=2)

    ax.view_init(azim=120, elev=30)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    plt.show()

ZOOM = 1
if __name__ == "__main__":
    # mountain_range = generate_mountain_range(10)
    mountain_range = imgToPrunedMatrix(7, 50, './matrix/denaliHeightMap.png')
    mountain_range = zoom(mountain_range, (ZOOM, ZOOM))
    local_min_path_naive = find_local_min(mountain_range)
    local_min_path_sgd = find_local_min_sgd(mountain_range, 3)

    plot_topography_3d(mountain_range, local_min_path_sgd)
    plt.colorbar()
    plt.show()
