import numpy as np

def get_cube_mesh(edge=1.0):
    h = edge / 2.0
    # Vértices centrados na origem para facilitar transformações futuras
    vertices = np.array([
        [-h, -h, -h], [h, -h, -h], [h, h, -h], [-h, h, -h],
        [-h, -h, h],  [h, -h, h],  [h, h, h],  [-h, h, h]
    ])
    
    # 12 triângulos (2 por face)
    faces = [
        [0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], # Base e Topo
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6], # Frente e Trás
        [1, 2, 6], [1, 6, 5], [3, 0, 4], [3, 4, 7]  # Laterais
    ]
    return vertices, faces