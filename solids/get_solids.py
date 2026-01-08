import numpy as np
from solids.cubo import get_cube_mesh
from solids.torus import get_torus_mesh
from solids.hermite import get_hermite_mesh

def get_solids():
    v_cube, f_cube = get_cube_mesh(edge=2.0)
    
    p0 = np.array([-4, 0, 0])
    p1 = np.array([4, 0, 0])

    t0 = np.array([0, 20, 0])  # Sobe reto
    t1 = np.array([0, 20, 0])  # Chega subindo reto
    v_herm, f_herm = get_hermite_mesh(p0, p1, t0, t1, radius=0.3, steps=10)
    
    v_torus, f_torus = get_torus_mesh(r_inner=0.8, r_outer=2.0)
    v_cube = v_cube + np.array([-6, 0, 0])
    v_herm = v_herm + np.array([0, 4, 2])
    v_torus = v_torus + np.array([6, 0, 0])
    
    return {
        "cubo": (v_cube, f_cube),
        "hermite": (v_herm, f_herm),
        "toro": (v_torus, f_torus)
    }