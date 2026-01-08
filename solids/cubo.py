import numpy as np

def get_cube_mesh(edge=1.0):
    h = edge / 2.0
    vertices = np.array([
        [-h, -h, -h], [h, -h, -h], [h, h, -h], [-h, h, -h],
        [-h, -h, h],  [h, -h, h],  [h, h, h],  [-h, h, h]
    ])
    
    faces = [
        [0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], 
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6], 
        [1, 2, 6], [1, 6, 5], [3, 0, 4], [3, 4, 7]  
    ]
    return vertices, faces

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_cubo(edge, origin=(0, 0, 0)):
    ox, oy, oz = origin
    L = edge

    vertices = [
        (ox, oy, oz),
        (ox + L, oy, oz),
        (ox + L, oy + L, oz),
        (ox, oy + L, oz),
        (ox, oy, oz + L),
        (ox + L, oy, oz + L),
        (ox + L, oy + L, oz + L),
        (ox, oy + L, oz + L)
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    return vertices, edges


def plot_cubo(ax, vertices, edges, color="black", show_vertices=True):
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    # Plot dos vértices
    if show_vertices:
        ax.scatter(xs, ys, zs, color="red", s=50)

        # Rótulos
        for i, (x, y, z) in enumerate(vertices):
            ax.text(x, y, z, f'{i}', fontsize=9)

    # Plot das arestas
    for i, j in edges:
        p1 = vertices[i]
        p2 = vertices[j]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color=color
        )

def cube_to_triangle_mesh(vertices):
    faces = [
        [0, 2, 1], [0, 3, 2],
        [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4],
        [2, 3, 7], [2, 7, 6],
        [1, 2, 6], [1, 6, 5],
        [3, 0, 4], [3, 4, 7]
    ]
    return vertices, faces


def plot_triangle_mesh(ax, vertices, faces, color='pink'):
    triangles = [[vertices[i] for i in face] for face in faces]
    mesh = Poly3DCollection(
        triangles,
        facecolor=color,
        edgecolor='black',
        alpha=0.6
    )
    ax.add_collection3d(mesh)