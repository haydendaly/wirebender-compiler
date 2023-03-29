import random
import math
from typing import List, Tuple
import numpy as np
from noise import pnoise2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def generate_mountain_range(size: int, scale: float = 0.05, octaves: int = 2, persistence: float = 2, lacunarity: float = 0.5):
    mountain_range = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            mountain_range[i, j] = pnoise2(i * scale, j * scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=size, repeaty=size)
    mountain_range = (mountain_range - mountain_range.min()) / (mountain_range.max() - mountain_range.min())
    return mountain_range * 10

def find_local_min(mountain_range: np.ndarray) -> list:
    height, width = mountain_range.shape
    i = height // 2
    j = height // 2
    path = [((i, j), 0, 0)]

    def neighbors(i, j):
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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
        height_diff = current_height - min_height
        hypotenuse = np.sqrt(height_diff ** 2 + 1)
        angle = np.degrees(np.arcsin(height_diff / hypotenuse))
        path.append(((ni, nj), hypotenuse, angle))
        i, j = ni, nj

    return path

def path_to_wirebender_format(path: list) -> str:
    wirebender_commands = []

    for i in range(len(path) - 1):
        p1, p2 = np.array(path[i]), np.array(path[i + 1])
        diff = p2 - p1

        feed = np.linalg.norm(diff)
        wirebender_commands.append(f"feed {feed:.2f}")

        if i < len(path) - 2:
            p3 = np.array(path[i + 2])
            v1, v2 = p2 - p1, p3 - p2
            bend_angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
            wirebender_commands.append(f"bend {bend_angle:.2f}")

            v1_xy, v2_xy = v1.copy(), v2.copy()
            v1_xy[2] = 0
            v2_xy[2] = 0
            rotate_angle = np.degrees(np.arccos(np.dot(v1_xy, v2_xy) / (np.linalg.norm(v1_xy) * np.linalg.norm(v2_xy))))
            rotate_angle = round(rotate_angle / 90) * 90
            wirebender_commands.append(f"rotate {rotate_angle:.2f}")

    return "\n".join(wirebender_commands)


def plot_topography(mountain_range: np.ndarray, local_min_path: list = None):
    fig, ax = plt.subplots()
    img = ax.imshow(mountain_range, cmap="terrain")
    fig.colorbar(img, ax=ax)

    if local_min_path:
        y_coords, x_coords = zip(*[coord for coord, _, _ in local_min_path])
        ax.plot(x_coords, y_coords, marker='o', markersize=5, linestyle='-', color='red', linewidth=2)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.show()

def plot_topography_3d(mountain_range: np.ndarray, local_min_path: list = None):
    step = 1
    X, Y = np.meshgrid(np.arange(0, len(mountain_range), step), np.arange(0, len(mountain_range), step))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, mountain_range, cmap="terrain", alpha=0.7)
    if local_min_path:
        x_coords, y_coords, z_coords = zip(*[(x, y, mountain_range[y, x]) for (x, y), _, _ in local_min_path])
        ax.plot(x_coords, y_coords, z_coords, marker='o', markersize=5, linestyle='-', color='red', linewidth=2)

    ax.view_init(azim=120, elev=30)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    plt.show()

if __name__ == "__main__":
    mountain_range = generate_mountain_range(10)
    local_min_path = find_local_min(mountain_range)

    plot_topography_3d(mountain_range, local_min_path)
    plt.colorbar()
    plt.show()
