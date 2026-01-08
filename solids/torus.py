import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def get_torus_mesh(r_inner, r_outer, nu=10, nv=10):
    R = (r_outer + r_inner) / 2.0
    r = (r_outer - r_inner) / 2.0
    
    u = np.linspace(0, 2*np.pi, nu)
    v = np.linspace(0, 2*np.pi, nv)
    U, V = np.meshgrid(u, v)
    
    X = (R + r * np.cos(U)) * np.cos(V)
    Y = (R + r * np.cos(U)) * np.sin(V)
    Z = r * np.sin(U)
    
    vertices = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
    
    faces = []
    for j in range(nv - 1):
        for i in range(nu - 1):
            p0, p1 = j*nu + i, j*nu + (i + 1)
            p2, p3 = (j+1)*nu + (i+1), (j+1)*nu + i
            faces.extend([[p0, p1, p2], [p0, p2, p3]])
            
    return vertices, faces


def create_torus(inner_radius, outer_radius, resolution=20, origin=(0, 0, 0)):
    if inner_radius <= 0 or outer_radius <= 0:
        raise ValueError("Os raios devem ser positivos.")

    ox, oy, oz = origin
    r = inner_radius
    R = outer_radius

    u = np.linspace(0, 2 * np.pi, resolution, endpoint=False)
    v = np.linspace(0, 2 * np.pi, resolution, endpoint=False)

    vertices = []

    for i in range(resolution):
        for j in range(resolution):
            x = (R + r * np.cos(v[j])) * np.cos(u[i]) + ox
            y = (R + r * np.cos(v[j])) * np.sin(u[i]) + oy
            z = r * np.sin(v[j]) + oz
            vertices.append((x, y, z))

    edges = []
    for i in range(resolution):
        for j in range(resolution):
            current = i * resolution + j
            right = i * resolution + (j + 1) % resolution
            down = ((i + 1) % resolution) * resolution + j

            edges.append((current, right))
            edges.append((current, down))

    return vertices, edges

def plot_torus(ax, vertices, edges, color="black", show_vertices=False):
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    # Vértices
    if show_vertices:
        ax.scatter(xs, ys, zs, color="red", s=20)
        for i, (x, y, z) in enumerate(vertices):
            ax.text(x, y, z, f'{i}', fontsize=7)

    # Arestas
    for i, j in edges:
        p1 = vertices[i]
        p2 = vertices[j]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color=color,
            linewidth=0.8
        )

def set_equal_axes(ax, vertices):
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    max_range = max(
        max(xs) - min(xs),
        max(ys) - min(ys),
        max(zs) - min(zs)
    ) / 2

    mid_x = (max(xs) + min(xs)) / 2
    mid_y = (max(ys) + min(ys)) / 2
    mid_z = (max(zs) + min(zs)) / 2

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

def torus_to_triangle_mesh(vertices, resolution_u, resolution_v):
    faces = []

    for i in range(resolution_u):
        for j in range(resolution_v):
            a = i * resolution_v + j
            b = i * resolution_v + (j + 1) % resolution_v
            c = ((i + 1) % resolution_u) * resolution_v + (j + 1) % resolution_v
            d = ((i + 1) % resolution_u) * resolution_v + j

            faces.append([a, b, c])
            faces.append([a, c, d])

    return vertices, faces

def plot_triangle_mesh(ax, vertices, faces, color="yellow"):
    triangles = [[vertices[i] for i in face] for face in faces]

    mesh = Poly3DCollection(
        triangles,
        facecolor=color,
        edgecolor="black",
        alpha=0.6
    )

    ax.add_collection3d(mesh)