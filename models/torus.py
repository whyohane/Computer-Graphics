import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_torus_mesh(r_inner, r_outer, nu=10, nv=10):
    R = (r_outer + r_inner) / 2.0
    r = (r_outer - r_inner) / 2.0
    
    # Gera a malha de parâmetros
    u = np.linspace(0, 2*np.pi, nu)
    v = np.linspace(0, 2*np.pi, nv)
    U, V = np.meshgrid(u, v)
    
    # Equações paramétricas vetorizadas
    X = (R + r * np.cos(U)) * np.cos(V)
    Y = (R + r * np.cos(U)) * np.sin(V)
    Z = r * np.sin(U)
    
    vertices = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
    
    # Conectividade das faces (triângulos)
    faces = []
    for j in range(nv - 1):
        for i in range(nu - 1):
            p0, p1 = j*nu + i, j*nu + (i + 1)
            p2, p3 = (j+1)*nu + (i+1), (j+1)*nu + i
            faces.extend([[p0, p1, p2], [p0, p2, p3]])
            
    return vertices, faces