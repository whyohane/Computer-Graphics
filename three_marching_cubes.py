import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# UTILITÁRIOS MATEMÁTICOS
# ==========================================
def vec_add(v1, v2): return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]
def vec_mul(v, s): return [v[0]*s, v[1]*s, v[2]*s]
def vec_cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def vec_len(v): return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
def vec_norm(v):
    l = vec_len(v)
    return [v[0]/l, v[1]/l, v[2]/l] if l > 0 else [0,0,0]

# Função nova para mover os objetos
def apply_translation(vertices, tx, ty, tz):
    """Soma um valor (tx, ty, tz) a cada vértice da lista."""
    new_verts = []
    for v in vertices:
        new_verts.append([v[0] + tx, v[1] + ty, v[2] + tz])
    return new_verts

# ==========================================
# 1. ALGORITMO: CUBO
# ==========================================
def get_cube_mesh(edge, origin=(0,0,0)):
    ox, oy, oz = origin
    L = edge
    vertices = [
        (ox, oy, oz), (ox+L, oy, oz), (ox+L, oy+L, oz), (ox, oy+L, oz),
        (ox, oy, oz+L), (ox+L, oy, oz+L), (ox+L, oy+L, oz+L), (ox, oy+L, oz+L)
    ]
    faces = [
        [0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
        [1, 2, 6], [1, 6, 5], [3, 0, 4], [3, 4, 7]
    ]
    return vertices, faces

# ==========================================
# 2. ALGORITMO: CANO DE HERMITE
# ==========================================
def hermite_point(t, P0, P1, T0, T1):
    h1 = 2*t**3 - 3*t**2 + 1
    h2 = -2*t**3 + 3*t**2
    h3 = t**3 - 2*t**2 + t
    h4 = t**3 - t**2
    return vec_add(vec_add(vec_mul(P0, h1), vec_mul(P1, h2)), vec_add(vec_mul(T0, h3), vec_mul(T1, h4)))

def hermite_tangent(t, P0, P1, T0, T1):
    dh1 = 6*t**2 - 6*t
    dh2 = -6*t**2 + 6*t
    dh3 = 3*t**2 - 4*t + 1
    dh4 = 3*t**2 - 2*t
    res = vec_add(vec_add(vec_mul(P0, dh1), vec_mul(P1, dh2)), vec_add(vec_mul(T0, dh3), vec_mul(T1, dh4)))
    return vec_norm(res)

def get_hermite_mesh(P0, P1, T0, T1, radius, steps=40, resolution=10):
    vertices = []
    faces = []
    rings = []
    global_up = [0, 0, 1]

    for i in range(steps + 1):
        t = i / float(steps)
        center = hermite_point(t, P0, P1, T0, T1)
        tangent = hermite_tangent(t, P0, P1, T0, T1)
        
        right = vec_cross(tangent, global_up)
        if vec_len(right) < 0.001: right = vec_cross(tangent, [1, 0, 0])
        right = vec_norm(right)
        up_local = vec_norm(vec_cross(right, tangent))
        
        idx_start = len(vertices)
        for j in range(resolution):
            angle = 2 * math.pi * j / resolution
            r_vec = vec_mul(right, math.cos(angle) * radius)
            u_vec = vec_mul(up_local, math.sin(angle) * radius)
            vertices.append(vec_add(center, vec_add(r_vec, u_vec)))
        rings.append(range(idx_start, len(vertices)))

    for i in range(len(rings) - 1):
        r1 = rings[i]
        r2 = rings[i+1]
        for j in range(resolution):
            idx0, idx1 = r1[j], r1[(j+1)%resolution]
            idx2, idx3 = r2[j], r2[(j+1)%resolution]
            faces.append([idx0, idx1, idx2])
            faces.append([idx1, idx3, idx2])
            
    return vertices, faces

# ==========================================
# 3. ALGORITMO: TORO
# ==========================================
def get_torus_mesh(r_inner, r_outer, nu=20, nv=20):
    R = (r_outer + r_inner) / 2.0
    r = (r_outer - r_inner) / 2.0
    vertices = []
    faces = []

    for j in range(nv):
        phi = 2 * math.pi * j / nv
        for i in range(nu):
            theta = 2 * math.pi * i / nu
            dist = R + r * math.cos(theta)
            vertices.append([dist * math.cos(phi), dist * math.sin(phi), r * math.sin(theta)])
    
    for j in range(nv):
        for i in range(nu):
            p0 = j * nu + i
            p1 = j * nu + (i + 1) % nu
            p2 = ((j + 1) % nv) * nu + (i + 1) % nu
            p3 = ((j + 1) % nv) * nu + i
            faces.append([p0, p1, p3])
            faces.append([p1, p2, p3])
            
    return vertices, faces

# ==========================================
# VISUALIZAÇÃO UNIFICADA
# ==========================================
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d') # APENAS UM PLOT

# --- 1. Preparar o Cubo ---
v_cube, f_cube = get_cube_mesh(edge=3, origin=(-1.5, -1.5, -1.5)) # Centrado na origem local
# Mover para a Esquerda (X = -10)
v_cube = apply_translation(v_cube, -10, 0, 0)

# --- 2. Preparar o Hermite ---
v_herm, f_herm = get_hermite_mesh([0,0,0], [5,5,5], [0,10,0], [10,0,0], radius=0.8)
# Deixar no Centro (X ~ 0) - Pequeno ajuste para centralizar visualmente
v_herm = apply_translation(v_herm, -2, -2, 0)

# --- 3. Preparar o Toro ---
v_tor, f_tor = get_torus_mesh(r_inner=1, r_outer=3, nu=20, nv=30)
# Mover para a Direita (X = +10)
v_tor = apply_translation(v_tor, 10, 0, 0)


# --- Plotagem de Todos ---

# Plot Cubo
ax.plot_trisurf([v[0] for v in v_cube], [v[1] for v in v_cube], [v[2] for v in v_cube], 
                 triangles=f_cube, color='cyan', alpha=0.8, edgecolor='k', linewidth=0.5)

# Plot Hermite
ax.plot_trisurf([v[0] for v in v_herm], [v[1] for v in v_herm], [v[2] for v in v_herm], 
                 triangles=f_herm, color='orange', alpha=0.8, edgecolor='k', linewidth=0.5)

# Plot Toro
ax.plot_trisurf([v[0] for v in v_tor], [v[1] for v in v_tor], [v[2] for v in v_tor], 
                 triangles=f_tor, color='lime', alpha=0.7, edgecolor='k', linewidth=0.5)

# Ajustes Finais da Cena
ax.set_title("Cena Unificada: Cubo, Hermite e Toro")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Ajuste de limites para caber tudo (de -15 a +15 no X)
ax.set_xlim(-15, 15)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)

plt.show()