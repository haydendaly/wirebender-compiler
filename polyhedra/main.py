import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv

def distance_between_points(a, b):
    return np.linalg.norm(a - b)

def get_neighbors(vertex, faces):
    neighbors = set()
    for face in faces:
        if vertex in face:
            neighbors.update(face)
    neighbors.remove(vertex)
    return list(neighbors)

def is_connected(vertex_a, vertex_b, faces):
    for face in faces:
        if vertex_a in face and vertex_b in face:
            return True
    return False

def min_path_to_visit_all_vertices(vertices, faces):
    n = len(vertices)
    visited = [False] * n
    visited[0] = True
    max_path, _ = dfs([0], visited, vertices, faces, 0)

    return max_path

def dfs(current_path, visited, vertices, faces, path_length):
    if all(visited):
        return current_path, len(current_path)

    max_path = current_path
    max_path_length = len(current_path)

    for i in range(len(vertices)):
        if not visited[i] and is_connected(current_path[-1], i, faces):
            visited[i] = True
            new_path, new_path_length = dfs(current_path + [i], visited, vertices, faces, path_length + distance_between_points(vertices[current_path[-1]], vertices[i]))
            if new_path_length > max_path_length:
                max_path = new_path
                max_path_length = new_path_length
            visited[i] = False

    return max_path, max_path_length


def traveling_salesman(vertices):
    num_vertices = len(vertices)
    distance_matrix = squareform(pdist(vertices))
    all_paths = list(permutations(range(num_vertices)))

    min_path, min_cost = None, float("inf")
    for path in all_paths:
        cost = sum(distance_matrix[path[i], path[i + 1]] for i in range(num_vertices - 1))
        if cost < min_cost:
            min_cost = cost
            min_path = path

    return min_path

def angle_between_vectors(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    cos_angle = dot_product / (magnitude_a * magnitude_b)
    angle = np.degrees(np.arccos(cos_angle))
    return angle

class Wire:
    def __init__(self):
        self.vertices = [(0, 0, 0)]
        self.direction = np.array([1, 0, 0])

    def rotate(self, angle):
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ])
        self.direction = rotation_matrix @ self.direction

    def bend(self, angle):
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ])
        self.direction = rotation_matrix @ self.direction

    def feed(self, value):
        displacement = value * self.direction
        self.vertices.append(self.vertices[-1] + displacement)

def wirebender_to_coordinates(wirebender_string: str):
    wire = Wire()

    wirebender_lines = wirebender_string.split('\n')

    for line in wirebender_lines:
        opcode, value = line.split()
        value = float(value)

        if opcode == 'feed':
            wire.feed(value)
        elif opcode == 'rotate':
            angle_a = np.radians(value)
            wire.rotate(angle_a)
        elif opcode == 'bend':
            angle_b = np.radians(value)
            wire.bend(angle_b)

    return wire.vertices


def plot_wirebender_path(wirebender_path: list):
    coordinates = wirebender_to_coordinates(wirebender_path)
    x, y, z = zip(*coordinates)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, marker='o', markersize=5, linestyle='-', color='red', linewidth=2)

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    plt.show()

def polyhedra_to_wirebender(vertices, faces, path):
    instructions = []
    for i in range(len(path) - 1):
        start_vertex = vertices[path[i]]
        end_vertex = vertices[path[i + 1]]
        angle = np.arccos(np.dot(start_vertex, end_vertex) / (np.linalg.norm(start_vertex) * np.linalg.norm(end_vertex)))
        axis = np.cross(start_vertex, end_vertex)
        axis /= np.linalg.norm(axis)
        rotation_angle = np.degrees(angle)
        instructions.append(f"rotate {rotation_angle:.2f}")
        instructions.append(f"bend {180 - 2 * rotation_angle:.2f}")
        feed_distance = np.linalg.norm(end_vertex - start_vertex)
        instructions.append(f"feed {feed_distance:.2f}")
    return "\n".join(instructions)

def generate_polyhedra(polyhedron_name):
    if polyhedron_name == 'tetrahedron':
        poly = pv.Tetrahedron()
    elif polyhedron_name == 'cube':
        poly = pv.Cube()
    elif polyhedron_name == 'octahedron':
        poly = pv.Octahedron()
    elif polyhedron_name == 'dodecahedron':
        poly = pv.Dodecahedron()
    elif polyhedron_name == 'icosahedron':
        poly = pv.Icosahedron()
    else:
        raise ValueError("Invalid polyhedron name")
    
    vertices = poly.points
    faces = poly.faces.reshape(-1, 4)[:, 1:]

    return vertices, faces

vertices, faces = generate_polyhedra("icosahedron")
path = min_path_to_visit_all_vertices(vertices, faces)
wirebender_script = polyhedra_to_wirebender(vertices, faces, path)
print(wirebender_script)
plot_wirebender_path(wirebender_script)
