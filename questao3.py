import numpy as np
import matplotlib.pyplot as plt

from utils import apply_transformation
from models.get_solids import get_solids

C = np.array([0, -10, 5])   # Posição da câmera
P = np.array([0, 0, 0])     # Look-at (Origem do mundo)
up = np.array([0, 0, 1])    # Vetor View-Up

def normalize(v):
    return v / np.linalg.norm(v)

# Construção da base (u, v, n) - Sistema da Câmera
z_cam = normalize(C - P)               # Eixo Z (aponta da cena para a câmera)
u_cam = normalize(np.cross(up, z_cam)) # Eixo X (lateral)
v_cam = np.cross(z_cam, u_cam)         # Eixo Y (vertical da câmera)

# 2. Matriz de Visualização (View Matrix) (Letra B) = np.array([0, -10, 5])   # posição da câmera
P = np.array([0, 0, 0])     # ponto observado (origem do mundo)
up = np.array([0, 0, 1])    # vetor up

def normalize(v):
    return v / np.linalg.norm(v)

z = normalize(C - P)                # eixo Z da câmera
u = normalize(np.cross(up, z))      # eixo X da câmera
v = np.cross(z, u)                  # eixo Y da câmera

def get_view_matrix(u, v, z, C):
    return np.array([
        [u[0], u[1], u[2], -np.dot(u, C)],
        [v[0], v[1], v[2], -np.dot(v, C)],
        [z[0], z[1], z[2], -np.dot(z, C)],
        [0,    0,    0,     1]
    ])

V = get_view_matrix(u, v, z, C)

scene_world = get_solids()

def transform_scene_to_camera(scene_world, view_matrix):
    scene_camera = {}
    for name, (v, f) in scene_world.items():
        v_cam = apply_transformation(v, view_matrix)
        scene_camera[name] = (v_cam, f)
    return scene_camera

scene_camera = transform_scene_to_camera(scene_world, V)

O_cam = apply_transformation(np.array([[0, 0, 0]]), V)

def plot_camera_scene(scene_camera, O_cam):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    colors = {
        "cubo": "cyan",
        "hermite": "orange",
        "toro": "lime"
    }

    # Plotar os objetos com transparência para não esconderem o ponto
    for name, (v, f) in scene_camera.items():
        ax.plot_trisurf(
            v[:, 0], v[:, 1], v[:, 2],
            triangles=f,
            color=colors.get(name, "gray"), # usa gray se não achar a cor
            edgecolor="k",
            alpha=0.3  # <--- IMPORTANTE: Transparência alta (0.3) para ver através
        )

    # --- AQUI ESTÁ A MUDANÇA PARA O PONTO ---
    
    # Coordenadas do ponto
    px, py, pz = O_cam[0, 0], O_cam[0, 1], O_cam[0, 2]

    # 1. Desenha a esfera do ponto bem grande (s=500)
    ax.scatter(
        px, py, pz,
        color='red',        # Cor vermelha chamativa
        s=500,              # <--- TAMANHO GIGANTE
        edgecolor='yellow', # Borda amarela para contraste
        linewidth=2,
        label="Origem do Mundo",
        depthshade=False    # Impede que o ponto fique escuro se estiver longe
    )

    # 2. Adiciona um texto flutuante apontando para o ponto
    ax.text(
        px, py, pz, 
        "  <-- ORIGEM (0,0,0)", 
        color='black', 
        fontsize=12, 
        fontweight='bold'
    )

    # Configurações dos eixos
    ax.set_title("Questão 3 – Cena no Sistema de Coordenadas da Câmera")
    ax.set_xlabel("Xc (Lateral)")
    ax.set_ylabel("Yc (Vertical)")
    ax.set_zlabel("Zc (Profundidade)")
    ax.legend()
    
    # Ajuste para proporção igual (evita distorção)
    ax.set_box_aspect([1, 1, 1]) 
    
    plt.show()

# Chame a função
plot_camera_scene(scene_camera, O_cam)