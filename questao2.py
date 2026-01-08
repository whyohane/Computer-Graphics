import numpy as np
import matplotlib.pyplot as plt
from solids.cubo import get_cube_mesh
from solids.torus import get_torus_mesh
from solids.hermite import get_hermite_mesh
from utils import get_translation_matrix, get_scale_matrix, get_rotation_z_matrix, apply_transformation

def calculate_scale_to_fit(vertices, target_size=3.0):
    max_val = np.abs(vertices).max()
    if max_val == 0:
        return 1.0
    return target_size / max_val

def questao_2_cena_mundo():
    scene = {}

    SAFE_SIZE = 2

    v_cube, f_cube = get_cube_mesh(edge=2.0)
    
    s_cube = calculate_scale_to_fit(v_cube, target_size=SAFE_SIZE)
    
    S = get_scale_matrix(s_cube, s_cube, s_cube) 
    R = get_rotation_z_matrix(np.pi / 6)         
    T = get_translation_matrix(-5, 0, 0)         
    
    M = T @ R @ S 
    scene["cubo"] = (apply_transformation(v_cube, M), f_cube)

   
    p0, p1 = np.array([-4,0,0]), np.array([4,0,0])
    t0, t1 = np.array([0,10,0]), np.array([0,10,0])
    v_herm, f_herm = get_hermite_mesh(p0, p1, t0, t1, radius=0.3)

    s_herm = calculate_scale_to_fit(v_herm, target_size=4.0) 
    
    S = get_scale_matrix(s_herm, s_herm, s_herm)
    R = get_rotation_z_matrix(np.pi / 2) 
    T = get_translation_matrix(0, 0, 0) 
    
    M = T @ R @ S
    scene["hermite"] = (apply_transformation(v_herm, M), f_herm)

    v_torus, f_torus = get_torus_mesh(r_inner=0.8, r_outer=2.0)
    
    s_torus = calculate_scale_to_fit(v_torus, target_size=SAFE_SIZE)
    
    S = get_scale_matrix(s_torus, s_torus, s_torus)
    R = get_rotation_z_matrix(np.pi / 4) 
    T = get_translation_matrix(5, 0, 0)  
    
    M = T @ R @ S
    scene["toro"] = (apply_transformation(v_torus, M), f_torus)

    return scene

def plot_scene(scene):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    colors = {"cubo": "cyan", "hermite": "orange", "toro": "lime"}

    max_coord_found = 0

    for name, (v, f) in scene.items():
        curr_max = np.abs(v).max()
        if curr_max > max_coord_found: max_coord_found = curr_max
        
        ax.plot_trisurf(
            v[:, 0], v[:, 1], v[:, 2],
            triangles=f,
            color=colors.get(name, 'gray'),
            edgecolor="k",
            linewidth=0.5,
            alpha=0.7
        )

    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_zlim(-8, 8)
    ax.set_box_aspect([1, 1, 1])

    ax.set_title(f"Questão 2 – Cena no Mundo")
                 
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()

if __name__ == "__main__":
    cena = questao_2_cena_mundo()
    plot_scene(cena)