import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_cube(edge, origin=(0, 0, 0)):
    """
    Gera a estrutura de dados de um cubo.

    Args:
      edge (float): Comprimento da aresta.
      origin (tuple): Coordenadas (x, y, z) de um vértice da base.

    Returns:
      tuple: (vertices, arestas, faces)
    """
    ox, oy, oz = origin
    L = edge

    # 1. Vértices
    vertices = [
        (ox, oy, oz),             # 0
        (ox + L, oy, oz),         # 1
        (ox + L, oy + L, oz),     # 2
        (ox, oy + L, oz),         # 3
        (ox, oy, oz + L),         # 4
        (ox + L, oy, oz + L),     # 5
        (ox + L, oy + L, oz + L), # 6
        (ox, oy + L, oz + L)      # 7
    ]

    # 2. Arestas
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Base inferior
        (4, 5), (5, 6), (6, 7), (7, 4),  # Base superior
        (0, 4), (1, 5), (2, 6), (3, 7)   # Colunas verticais
    ]

    # 3. Faces
    faces = [
        [0, 1, 2, 3],  # Fundo
        [4, 5, 6, 7],  # Topo
        [0, 1, 5, 4],  # Frente
        [2, 3, 7, 6],  # Trás
        [1, 2, 6, 5],  # Direita
        [3, 0, 4, 7]   # Esquerda
    ]

    return vertices, edges, faces


# ---------------- EXECUÇÃO ----------------

# Parâmetros do cubo
aresta = 3
origem = (1, 1, 1)

# Geração do modelo
verts, arestas, faces_idx = create_cube(aresta, origem)

# Separação das coordenadas
xs = [v[0] for v in verts]
ys = [v[1] for v in verts]
zs = [v[2] for v in verts]

# Criação da figura 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# 1. Plotar vértices
ax.scatter(xs, ys, zs, color='red', s=50, label='Vértices')

# Rótulos dos vértices
for i, (x, y, z) in enumerate(verts):
    ax.text(x, y, z, f'{i}', fontsize=12, color='black')

# 2. Plotar arestas
for start, end in arestas:
    p1 = verts[start]
    p2 = verts[end]
    ax.plot(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        [p1[2], p2[2]],
        color='blue'
    )

# Labels e título
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Cubo')

# ✅ CORREÇÃO DA ESCALA (ESSENCIAL)
ax.set_box_aspect([1, 1, 1])

plt.legend()
plt.show()

# ---------------- SAÍDA TEXTUAL ----------------

print("--- Definição Geométrica ---")
print(f"Vértices (Total {len(verts)}): {verts}")
print(f"Arestas (Total {len(arestas)}): {arestas}")
print(f"Exemplo de Face (índices): {faces_idx[0]}")

