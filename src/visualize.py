import re
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import CubicSpline

def read_script(file_path: str) -> str:
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def rotate_vector(vec, axis, angle_deg):
    angle_rad = np.radians(angle_deg)
    rotation_matrix = np.identity(3)

    if axis == 'z':
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1]
        ])
    elif axis == 'y':
        rotation_matrix = np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)]
        ])

    return np.matmul(rotation_matrix, vec)

def process_opcodes(opcodes: str) -> list:
    commands = opcodes.splitlines()
    x, y, z = 0, 0, 0
    direction = np.array([1, 0, 0])

    path = [(x, y, z)]

    for cmd in commands:
        operation, value = re.match(r"(\w+)\s+(-?\d+)", cmd).groups()
        value = float(value)

        if operation == "feed":
            x += value * direction[0]
            y += value * direction[1]
            z += value * direction[2]
            path.append((x, y, z))
        elif operation == "bend":
            direction = rotate_vector(direction, 'z', value)
        elif operation == "rotate":
            direction = rotate_vector(direction, 'y', value)

    return path


def plot_path(path: list):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_coords, y_coords, z_coords = zip(*path)
    ax.plot(x_coords, y_coords, z_coords, marker='o', linestyle='-', markersize=5)

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.view_init(azim=-120, elev=30) # isometric

    plt.show()

def plot_path_smooth(path: list):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x_coords, y_coords, z_coords = zip(*path)
    t = [0]
    for i in range(1, len(path)):
        t.append(t[-1] + np.linalg.norm(np.array(path[i]) - np.array(path[i - 1])))
    t = np.array(t)
    # catmull-rom
    spline_x = CubicSpline(t, x_coords, bc_type='natural')
    spline_y = CubicSpline(t, y_coords, bc_type='natural')
    spline_z = CubicSpline(t, z_coords, bc_type='natural')

    t_fine = np.linspace(t.min(), t.max(), 1000)
    x_coords_fine = spline_x(t_fine)
    y_coords_fine = spline_y(t_fine)
    z_coords_fine = spline_z(t_fine)

    ax.plot(x_coords_fine, y_coords_fine, z_coords_fine, linestyle='-', markersize=5)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.view_init(azim=-120, elev=30)
    plt.show()

if __name__ == "__main__":
    opcodes = read_script("./output/spring.wirec")
    path = process_opcodes(opcodes)
    plot_path_smooth(path)
