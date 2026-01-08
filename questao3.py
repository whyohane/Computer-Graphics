import numpy as np
import matplotlib.pyplot as plt
import math

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from questao2 import questao_2_cena_mundo
from utils import apply_transformation

def normalize(v):
        norm = math.sqrt(sum(coord * coord for coord in v))
        return [coord / norm for coord in v] if norm != 0 else v
    
def transform_to_camera(vertices, E, R):
    transformed = []
    for v in vertices:
        v_shift = [v[i] - E[i] for i in range(3)]
        v_cam = [
            v_shift[0] * R[0][0] + v_shift[1] * R[0][1] + v_shift[2] * R[0][2],
            v_shift[0] * R[1][0] + v_shift[1] * R[1][1] + v_shift[2] * R[1][2],
            v_shift[0] * R[2][0] + v_shift[1] * R[2][1] + v_shift[2] * R[2][2]
        ]
        transformed.append(v_cam)
    return np.array(transformed)

    
def compute_camera_matrix(eye, at, up):
    n = normalize([at[i] - eye[i] for i in range(3)])
    u = normalize([
        n[1] * up[2] - n[2] * up[1],
        n[2] * up[0] - n[0] * up[2],
        n[0] * up[1] - n[1] * up[0]
    ])
    v = [
        u[1] * n[2] - u[2] * n[1],
        u[2] * n[0] - u[0] * n[2],
        u[0] * n[1] - u[1] * n[0]
    ]
    return [u, v, [-n[0], -n[1], -n[2]]]

scene = questao_2_cena_mundo()
eye = [6, 6, 6]     # posição da câmera
at  = [0, 0, 0]     # ponto observado
up  = [0, 0, 1]     # eixo vertical
R = compute_camera_matrix(eye, at, up)
scene_cam = {}

for name, (v, f) in scene.items():
    v_cam = transform_to_camera(v, eye, R)
    scene_cam[name] = (v_cam, f)

def plot_camera_origin(ax, color="red"):
    ax.scatter(
        0, 0, 0,
        color=color,
        s=80,
        marker='o',
        depthshade=True,
        label="Câmera"
    )

def plot_scene_camera(scene):
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    colors = {"cubo": "cyan", "hermite": "orange", "toro": "lime"}

    for name, (v, f) in scene.items():
        ax.plot_trisurf(
            v[:, 0], v[:, 1], v[:, 2],
            triangles=f,
            color=colors.get(name, 'gray'),
            edgecolor="k",
            alpha=0.7
        )

    ax.set_title("Questão 3 – Cena no Sistema de Coordenadas da Câmera")
    ax.set_xlabel("Xc")
    ax.set_ylabel("Yc")
    ax.set_zlabel("Zc")
    ax.set_box_aspect([1, 1, 1])
    plot_camera_origin(ax)

    plt.show()

scene = questao_2_cena_mundo()
scene_cam = {}

R = compute_camera_matrix(eye, at, up)

for name, (v, f) in scene.items():
    scene_cam[name] = (transform_to_camera(v, eye, R), f)

plot_scene_camera(scene_cam)
