import numpy as np
from models.cubo import get_cube_mesh
from models.torus import get_torus_mesh
from models.hermite import get_hermite_mesh

def get_solids():
    # 1. Gerar os modelos brutos (todos nascem na origem 0,0,0)
    v_cube, f_cube = get_cube_mesh(edge=2.0)
    
    p0 = np.array([-4, 0, 0])
    p1 = np.array([4, 0, 0])

# Tangentes menores e mais "verticais" para o S não ficar gordo demais
    t0 = np.array([0, 20, 0])  # Sobe reto
    t1 = np.array([0, 20, 0])  # Chega subindo reto
    v_herm, f_herm = get_hermite_mesh(p0, p1, t0, t1, radius=0.3, steps=30)
    
    v_torus, f_torus = get_torus_mesh(r_inner=0.8, r_outer=2.0)
    
    # 2. ESPAÇAMENTO (Translação)
    # Somamos valores aos eixos X, Y ou Z para "empurrar" os objetos
    
    # Cubo vai para a esquerda (X negativo)
    v_cube = v_cube + np.array([-6, 0, 0])
    
    # Hermite fica no centro (apenas um ajuste se necessário)
    v_herm = v_herm + np.array([0, 4, 2])
    
    # Toro vai para a direita (X positivo)
    v_torus = v_torus + np.array([6, 0, 0])
    
    return {
        "cubo": (v_cube, f_cube),
        "hermite": (v_herm, f_herm),
        "toro": (v_torus, f_torus)
    }