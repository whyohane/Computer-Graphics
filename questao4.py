import numpy as np
import matplotlib.pyplot as plt
from questao2 import questao_2_cena_mundo
from utils import get_translation_matrix, apply_transformation

def perspective_project(v, d=1.0):
    x, y, z = v
    if z <= 0:
        return None
    return [-d * x / z, -d * y / z]


def extract_edges(faces):
    edges = set()
    for a, b, c in faces:
        edges.add(tuple(sorted((a, b))))
        edges.add(tuple(sorted((b, c))))
        edges.add(tuple(sorted((c, a))))
    return list(edges)


def plot_scene_perspective(scene_camera, d=1.0):
    fig, ax = plt.subplots(figsize=(8, 8))

    colors = {
        "cubo": "blue",
        "hermite": "orange",
        "toro": "green"
    }

    for name, (vertices, faces) in scene_camera.items():
        projected = [perspective_project(v, d) for v in vertices]
        edges = extract_edges(faces)

        for i, j in edges:
            if projected[i] is not None and projected[j] is not None:
                ax.plot(
                    [projected[i][0], projected[j][0]],
                    [projected[i][1], projected[j][1]],
                    color=colors.get(name, "black")
                )

    ax.set_title("Questão 4 – Projeção em Perspectiva (2D)")
    ax.set_xlabel("Xp")
    ax.set_ylabel("Yp")
    ax.set_aspect("equal")
    ax.grid(True)

    plt.show()


scene_world = questao_2_cena_mundo()

T_cam = get_translation_matrix(0, 0, 10)

scene_camera = {}
for name, (v, f) in scene_world.items():
    scene_camera[name] = (apply_transformation(v, T_cam), f)

plot_scene_perspective(scene_camera, d=5.0)