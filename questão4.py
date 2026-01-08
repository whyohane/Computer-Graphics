import numpy as np
import matplotlib.pyplot as plt

from models.get_solids import get_solids

def perspective_projection(vertices, f=5.0):
    """
    Projeta vértices 3D (no sistema da câmera) para 2D.
    Retorna array (N, 2)
    """
    projected = []

    for x, y, z in vertices:
        if z <= 0:
            projected.append([np.nan, np.nan])  # fora do volume de visão
        else:
            xp = f * x / z
            yp = f * y / z
            projected.append([xp, yp])

    return np.array(projected)


def extract_edges(faces):
    edges = set()
    for f in faces:
        a, b, c = f
        edges.add(tuple(sorted((a, b))))
        edges.add(tuple(sorted((b, c))))
        edges.add(tuple(sorted((c, a))))
    return list(edges)

def plot_scene_2d(scene_camera):
    fig, ax = plt.subplots(figsize=(8, 8))

    colors = {
        "cubo": "blue",
        "hermite": "orange",
        "toro": "green"
    }

    for name, (v_cam, faces) in scene_camera.items():
        v_2d = perspective_projection(v_cam, f=5.0)
        edges = extract_edges(faces)

        for i, j in edges:
            if not np.any(np.isnan(v_2d[[i, j]])):
                ax.plot(
                    [v_2d[i, 0], v_2d[j, 0]],
                    [v_2d[i, 1], v_2d[j, 1]],
                    color=colors[name]
                )

    ax.set_title("Projeção em Perspectiva – Cena 2D")
    ax.set_xlabel("Xp")
    ax.set_ylabel("Yp")
    ax.set_aspect("equal")
    ax.grid(True)

    plt.show()

plot_scene_2d(get_solids())
