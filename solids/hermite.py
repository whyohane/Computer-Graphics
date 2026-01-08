import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def get_hermite_mesh(P0, P1, T0, T1, radius=0.3, steps=40, resolution=8):
    t = np.linspace(0, 1, steps).reshape(-1, 1)
    
    h1 = 2*t**3 - 3*t**2 + 1
    h2 = -2*t**3 + 3*t**2
    h3 = t**3 - 2*t**2 + t
    h4 = t**3 - t**2
    
    path = h1*P0 + h2*P1 + h3*T0 + h4*T1
    
    dh1 = 6*t**2 - 6*t
    dh2 = -6*t**2 + 6*t
    dh3 = 3*t**2 - 4*t + 1
    dh4 = 3*t**2 - 2*t
    tangents = dh1*P0 + dh2*P1 + dh3*T0 + dh4*T1
    
    vertices = []
    for i in range(steps):
        p, tan = path[i], tangents[i]
        tan /= np.linalg.norm(tan)
        
        up = np.array([0,0,1]) if abs(tan[2]) < 0.9 else np.array([1,0,0])
        side = np.cross(tan, up)
        side /= np.linalg.norm(side)
        up_final = np.cross(side, tan)
        
        angles = np.linspace(0, 2*np.pi, resolution, endpoint=False)
        for a in angles:
            v = p + radius * (np.cos(a)*side + np.sin(a)*up_final)
            vertices.append(v)
            
    faces = []
    for i in range(steps - 1):
        for j in range(resolution):
            p0, p1 = i*resolution + j, i*resolution + (j+1)%resolution
            p2, p3 = (i+1)*resolution + (j+1)%resolution, (i+1)*resolution + j
            faces.extend([[p0, p1, p2], [p0, p2, p3]])
            
    return np.array(vertices), faces


HERMITE_MATRIX = np.array([
    [ 2, -2,  1,  1],
    [-3,  3, -2, -1],
    [ 0,  0,  1,  0],
    [ 1,  0,  0,  0],
])

def hermite_coefficients(P1, P2, T1, T2):
    G = np.vstack([P1, P2, T1, T2])
    return HERMITE_MATRIX @ G

def hermite_cubic(t, HG):
    a, b, c, d = HG
    return a*t**3 + b*t**2 + c*t + d

def hermite_cubic_derivative(t, HG):
    a, b, c, _ = HG
    return 3*a*t**2 + 2*b*t + c

# ---------------- CRIA CANO ----------------
def create_pipe(control_points, radius=0.3, curve_resolution=20, circle_resolution=8):
    P1, P2, T1, T2 = map(np.array, control_points)
    coeffs = hermite_coefficients(P1, P2, T1, T2)

    t_vals = np.linspace(0, 1, curve_resolution)
    curve_pts = np.array([hermite_cubic(t, coeffs) for t in t_vals])
    tangents = np.array([hermite_cubic_derivative(t, coeffs) for t in t_vals])
    tangents = np.array([v / np.linalg.norm(v) for v in tangents])

    # Frame inicial
    T0 = tangents[0]
    ref = np.array([0, 0, 1])
    if abs(np.dot(T0, ref)) > 0.9:
        ref = np.array([1, 0, 0])

    N0 = np.cross(T0, ref)
    N0 /= np.linalg.norm(N0)
    B0 = np.cross(T0, N0)

    frames = [(T0, N0, B0)]

    for i in range(1, curve_resolution):
        _, N_prev, _ = frames[-1]
        T = tangents[i]
        v = N_prev - np.dot(N_prev, T) * T
        N = v / np.linalg.norm(v) if np.linalg.norm(v) > 1e-6 else N_prev
        B = np.cross(T, N)
        frames.append((T, N, B))

    vertices = []
    for i in range(curve_resolution):
        _, N, B = frames[i]
        center = curve_pts[i]
        for a in np.linspace(0, 2*np.pi, circle_resolution, endpoint=False):
            vertices.append(center + radius * (np.cos(a)*N + np.sin(a)*B))

    edges = []
    for i in range(curve_resolution):
        for j in range(circle_resolution):
            a = i * circle_resolution + j
            b = i * circle_resolution + (j + 1) % circle_resolution
            edges.append((a, b))

            if i < curve_resolution - 1:
                c = (i + 1) * circle_resolution + j
                edges.append((a, c))

    return np.array(vertices), edges

def plot_pipe(ax, vertices, edges, color="blue", show_vertices=True):
    if show_vertices:
        ax.scatter(
            vertices[:,0],
            vertices[:,1],
            vertices[:,2],
            color="red",
            s=2
        )

    for i, j in edges:
        p1 = vertices[i]
        p2 = vertices[j]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color=color
        )

def pipe_to_triangle_mesh(vertices, curve_resolution=20, circle_resolution=8):
   
    faces = []

    for i in range(curve_resolution - 1):
        for j in range(circle_resolution):
            a = i * circle_resolution + j
            b = i * circle_resolution + (j + 1) % circle_resolution
            c = (i + 1) * circle_resolution + (j + 1) % circle_resolution
            d = (i + 1) * circle_resolution + j

            faces.append([a, b, c])
            faces.append([a, c, d])

    return vertices, faces

def plot_triangle_mesh(ax, vertices, faces, color="magenta"):
    triangles = [[vertices[i] for i in face] for face in faces]

    mesh = Poly3DCollection(
        triangles,
        facecolor=color,
        edgecolor="black",
        alpha=0.6
    )

    ax.add_collection3d(mesh)