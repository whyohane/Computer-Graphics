import numpy as np

def get_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def get_scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ])

def get_rotation_z_matrix(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])

def apply_transformation(vertices, matrix):
    """
    Multiplica uma matriz 4x4 por vértices (N, 3).
    """
    # 1. Converte para coordenadas homogêneas (N, 4) adicionando uma coluna de 1s
    v_homo = np.append(vertices, np.ones((vertices.shape[0], 1)), axis=1)
    
    # 2. Multiplica: Matriz @ Vértices.T e depois transpõe de volta
    v_transformed = (matrix @ v_homo.T).T
    
    # 3. Retorna apenas as coordenadas (x, y, z)
    return v_transformed[:, :3]