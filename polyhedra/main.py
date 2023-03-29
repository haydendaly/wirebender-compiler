import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import permutations

def generate_polyhedron(vertices, faces):
    radius = 1
    vertices = (vertices / np.linalg.norm(vertices, axis=1)[:, np.newaxis]) * radius
    return vertices, faces

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

def polyhedron_to_wirebender_format(vertices, faces):
    min_path = traveling_salesman(vertices)
    path = [vertices[i] for i in min_path]
    path.append(path[0])  # Close the path
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
            wirebender_commands.append(f"rotate {rotate_angle:.2f}")

    return "\n".join(wirebender_commands)

# tetrahedron
vertices = np.array([
    [1, 1, 1],
    [1, -1, -1],
    [-1, 1, -1],
    [-1, -1, 1]
])

faces = [
    (0, 1, 2),
    (0, 1, 3),
    (0, 2, 3),
    (1, 2, 3)
]

vertices, faces = generate_polyhedron(vertices, faces)
wirebender_script = polyhedron_to_wirebender_format(vertices, faces)
print(wirebender_script)