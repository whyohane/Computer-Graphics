import numpy as np
import matplotlib.pyplot as plt

# Importando as fábricas de objetos
from models.cubo import get_cube_mesh
from models.torus import get_torus_mesh
from models.hermite import get_hermite_mesh
from utils import get_translation_matrix, get_scale_matrix, get_rotation_z_matrix, apply_transformation

def questao_1():
    # 1. Gerar os modelos brutos (todos nascem na origem 0,0,0)
    v_cube, f_cube = get_cube_mesh(edge=2.0)
    
    p0 = np.array([-4, 0, 0])
    p1 = np.array([4, 0, 0])

# Tangentes menores e mais "verticais" para o S não ficar gordo demais
    t0 = np.array([0, 20, 0])  # Sobe reto
    t1 = np.array([0, 20, 0])  # Chega subindo reto
    v_herm, f_herm = get_hermite_mesh(p0, p1, t0, t1, radius=0.3, steps=150)
    
    v_torus, f_torus = get_torus_mesh(r_inner=0.8, r_outer=2.0)
    
    # 2. ESPAÇAMENTO (Translação)
    # Somamos valores aos eixos X, Y ou Z para "empurrar" os objetos
    
    # Cubo vai para a esquerda (X negativo)
    v_cube = v_cube + np.array([-6, 0, 0])
    
    # Hermite fica no centro (apenas um ajuste se necessário)
    v_herm = v_herm + np.array([0, 0, 0])
    
    # Toro vai para a direita (X positivo)
    v_torus = v_torus + np.array([6, 0, 0])
    
    return {
        "cubo": (v_cube, f_cube),
        "hermite": (v_herm, f_herm),
        "toro": (v_torus, f_torus)
    }
    
def plot_cena(objetos):
    """Função auxiliar para desenhar tudo o que foi gerado."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Cores para cada sólido
    cores = {"cubo": "cyan", "hermite": "orange", "toro": "lime"}
    
    for nome, (v, f) in objetos.items():
        # Lembre-se: v[:, 0] é X, v[:, 1] é Y, v[:, 2] é Z
        ax.plot_trisurf(v[:, 0], v[:, 1], v[:, 2], 
                        triangles=f, color=cores[nome], 
                        alpha=0.6, edgecolor='k', label=nome)

    ax.set_title("Questão 1: Modelagem de Sólidos com NumPy")
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.set_zlim(-5, 5)
    plt.show()
    

def questao_2(dados_q1):
    cena_final = {}
    
    # --- TRANSFORMANDO O CUBO ---
    v_c, f_c = dados_q1["cubo"]
    # Escala para garantir que cabe, Rotação para estilo, Translação para o canto
    m_cube = get_translation_matrix(-5, -5, 0) @ \
             get_rotation_z_matrix(np.pi/4) @ \
             get_scale_matrix(1.2, 1.2, 1.2)
    cena_final["cubo"] = (apply_transformation(v_c, m_cube), f_c)
    
    # --- TRANSFORMANDO O TORO ---
    v_t, f_t = dados_q1["toro"]
    # Posiciona no lado oposto
    m_torus = get_translation_matrix(5, 5, 2) @ get_scale_matrix(0.8, 0.8, 0.8)
    cena_final["toro"] = (apply_transformation(v_t, m_torus), f_t)
    
    # --- TRANSFORMANDO O HERMITE ---
    v_h, f_h = dados_q1["hermite"]
    # Centraliza e ajusta escala
    m_herm = get_translation_matrix(0, 0, -2) @ get_scale_matrix(1, 1, 1)
    cena_final["hermite"] = (apply_transformation(v_h, m_herm), f_h)
    
    return cena_final
    
def plot_cena(objetos):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Cores vivas para cada sólido
    cores = {"cubo": "cyan", "hermite": "orange", "toro": "lime"}
    
    for nome, (v, f) in objetos.items():
        # plot_trisurf com configurações de brilho melhores
        ax.plot_trisurf(v[:, 0], v[:, 1], v[:, 2], 
                        triangles=f, 
                        color=cores.get(nome, "blue"), 
                        alpha=0.9,       # Mais opaco para não ficar escuro
                        edgecolor='black', 
                        linewidth=0.1,
                        shade=True)      # Ativa o sombreado 3D

    # --- MELHORIAS DE VISUALIZAÇÃO ---
    
    # 1. Ajustar limites (diminuí um pouco para os objetos "encherem" mais a tela)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_zlim(-8, 8)

    # 2. ESCALA IGUAL (Muito importante para não deformar os objetos)
    ax.set_box_aspect([1, 1, 1]) 

    # 3. Remover o fundo cinza para dar mais contraste
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    plt.tight_layout()
    plt.show()
    
   # --- EXECUÇÃO ---
if __name__ == "__main__":
    # 1. Chamamos a função que você pediu
    dados_objetos = questao_1()
    
    # 2. Plotamos o resultado
    plot_cena(dados_objetos)
    