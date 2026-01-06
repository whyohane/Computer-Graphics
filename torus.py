import math

# --- 1. Funções Auxiliares de Matemática ---
# Como não temos numpy, usamos funções nativas do módulo math

def get_torus_matrices(r_inner, r_outer, segments_c=30, segments_a=30):
    """
    Gera as matrizes de dados de um toro.
    
    Args:
        r_inner: Raio do buraco (interno).
        r_outer: Raio total (externo).
        segments_c: Resolução do corte transversal (tubo).
        segments_a: Resolução do anel principal (volta completa).
        
    Returns:
        vertices: Lista de listas [[x,y,z], [x,y,z]...]
        faces: Lista de listas [[idx1, idx2, idx3]...]
    """
    
    # R: Raio Maior (Distância do centro do Toro ao centro do tubo)
    R = (r_outer + r_inner) / 2.0
    
    # r: Raio Menor (Raio do tubo em si)
    r = (r_outer - r_inner) / 2.0

    vertices = []
    
    # --- Passo A: Gerar a Matriz de Vértices ---
    # Imagine uma malha retangular que vamos enrolar duas vezes
    
    # Loop 'v' percorre o anel maior (0 a 360 graus)
    for j in range(segments_a):
        phi = 2 * math.pi * j / segments_a  # Ângulo do anel
        
        # Loop 'u' percorre o corte do tubo (0 a 360 graus)
        for i in range(segments_c):
            theta = 2 * math.pi * i / segments_c # Ângulo do tubo

            # Fórmula Paramétrica do Toro
            # O termo (R + r * cos(theta)) é a distância do ponto no tubo até o eixo Z central
            dist_centro = R + r * math.cos(theta)

            x = dist_centro * math.cos(phi)
            y = dist_centro * math.sin(phi)
            z = r * math.sin(theta)

            vertices.append([x, y, z])

    # --- Passo B: Gerar a Matriz de Conectividade (Faces) ---
    faces = []
    
    for j in range(segments_a):
        for i in range(segments_c):
            # Precisamos calcular os índices dos 4 pontos que formam um quadrado
            # na superfície do toro. Usamos o operador % (módulo) para garantir
            # que o último ponto se conecte de volta ao primeiro (fechar o círculo).
            
            # Índices da malha (linha atual e próxima, coluna atual e próxima)
            row_curr = j
            row_next = (j + 1) % segments_a
            
            col_curr = i
            col_next = (i + 1) % segments_c
            
            # Converter coordenadas da malha (row, col) para índice linear na lista única
            # Índice = Linha * Largura + Coluna
            p0 = row_curr * segments_c + col_curr      # Atual
            p1 = row_curr * segments_c + col_next      # Próximo no tubo
            p2 = row_next * segments_c + col_next      # Próximo no anel
            p3 = row_next * segments_c + col_curr      # Diagonal
            
            # Criar 2 triângulos para formar o quadrado (Quad)
            # Triângulo 1
            faces.append([p0, p1, p3])
            # Triângulo 2
            faces.append([p1, p2, p3])

    return vertices, faces

# --- Execução ---

raio_int = 2.0
raio_ext = 6.0
res_tubo = 20
res_anel = 40

# Gera os dados puros (listas de listas)
matriz_vertices, matriz_faces = get_torus_matrices(raio_int, raio_ext, res_tubo, res_anel)

# --- Exibição dos Dados (Primeiras 5 linhas) ---
print(f"Total de Vértices: {len(matriz_vertices)}")
print(f"Total de Faces: {len(matriz_faces)}")
print("\n--- Amostra da Matriz de Vértices (Primeiros 3) ---")
for v in matriz_vertices[:3]:
    print(f"[{v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f}]")

print("\n--- Amostra da Matriz de Faces (Primeiros 3 triângulos) ---")
for f in matriz_faces[:3]:
    print(f"Conecta índices: {f}")

# --- (Opcional) Visualização Rápida para provar que funciona ---
# Se você tiver matplotlib instalado, isso vai desenhar. 
# Se não, o código acima já resolveu a parte matemática.
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Desempacotar listas para plotar
    vx = [v[0] for v in matriz_vertices]
    vy = [v[1] for v in matriz_vertices]
    vz = [v[2] for v in matriz_vertices]
    
    ax.plot_trisurf(vx, vy, vz, triangles=matriz_faces, cmap='viridis', edgecolor='none', alpha=0.8)
    
    # Ajustar escala visual
    ax.set_xlim(-raio_ext, raio_ext)
    ax.set_ylim(-raio_ext, raio_ext)
    ax.set_zlim(-raio_ext, raio_ext)
    plt.show()
    
except ImportError:
    print("Matplotlib não encontrado. Apenas os dados foram calculados.")