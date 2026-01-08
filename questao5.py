import numpy as np
import matplotlib.pyplot as plt
from models.get_solids import get_solids
from utils import apply_transformation

# ==========================================
# 1. ESTRUTURAS DO ALGORITMO SCANLINE (LIVRO AZEVEDO/CONCI)
# ==========================================

class Aresta:
    def __init__(self, y_max, x_min, inc_x):
        self.y_max = int(y_max) # Até qual Y essa aresta vai
        self.x = x_min          # X atual (começa no X do Y_min)
        self.inc_x = inc_x      # O quanto X muda a cada passo Y (1/m)

    def __repr__(self):
        return f"Aresta(ymax={self.y_max}, x={self.x:.2f}, inc={self.inc_x:.2f})"

def scanline_fill(vertices, img_buffer, color_val):
    """
    Implementação do Algoritmo Scanline com ET e AET.
    vertices: Lista de pontos (x, y) do polígono (já nas coordenadas da tela).
    img_buffer: Matriz numpy onde vamos desenhar.
    color_val: Valor da cor para preencher.
    """
    height, width = img_buffer.shape
    
    # 1. Construir a Tabela Global de Arestas (ET - Edge Table)
    # Dicionário onde a chave é o Y_min da aresta
    ET = {} 
    
    n = len(vertices)
    for i in range(n):
        # Pega vértice atual e o próximo (fechando o ciclo)
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        
        # Ignorar arestas horizontais (dy = 0) pois não cruzam scanlines
        if int(p1[1]) == int(p2[1]):
            continue
            
        # Garante que p1 é o ponto inferior (y menor) e p2 o superior
        if p1[1] > p2[1]:
            p1, p2 = p2, p1
            
        y_min = int(p1[1])
        y_max = int(p2[1])
        x_min = p1[0]
        
        # Cálculo do 1/m (inverso da inclinação)
        # dx / dy
        inc_x = (p2[0] - p1[0]) / (p2[1] - p1[1])
        
        nova_aresta = Aresta(y_max, x_min, inc_x)
        
        if y_min not in ET:
            ET[y_min] = []
        ET[y_min].append(nova_aresta)

    # 2. Inicializar AET (Active Edge Table) vazia
    AET = []
    
    # Encontrar onde começa e termina a varredura
    if not ET: return # Polígono inválido ou só horizontal
    y_start = min(ET.keys())
    y_end = max(edge.y_max for edges in ET.values() for edge in edges)
    
    # 3. Laço de Varredura (Scanlines)
    for y in range(y_start, y_end + 1):
        if y >= height or y < 0: continue # Check de segurança
        
        # a. Mover arestas da ET[y] para a AET
        if y in ET:
            AET.extend(ET[y])
            
        # b. Remover arestas da AET onde y == y_max (arestas que terminaram)
        # Nota: O livro sugere remover quando y = y_max. 
        AET = [edge for edge in AET if edge.y_max > y]
        
        # c. Ordenar AET pela coordenada X
        AET.sort(key=lambda edge: edge.x)
        
        # d. Preencher pixels entre pares de arestas (paridade)
        # Pegamos de 2 em 2: (x0 -> x1), (x2 -> x3)...
        for i in range(0, len(AET), 2):
            if i + 1 < len(AET):
                x_start = int(np.ceil(AET[i].x))
                x_end = int(np.floor(AET[i+1].x))
                
                # Clipping horizontal simples
                x_start = max(0, x_start)
                x_end = min(width - 1, x_end)
                
                if x_end >= x_start:
                    img_buffer[y, x_start : x_end + 1] = color_val

        # e. Incrementar X de todas as arestas na AET (para a próxima linha)
        for edge in AET:
            edge.x += edge.inc_x

# ==========================================
# 2. PREPARAÇÃO DA CENA E CÂMERA
# ==========================================
def get_projected_scene():
    """
    Retorna a cena projetada em coordenadas normalizadas (-1 a 1 aproximadamente).
    Reaproveita a lógica da Questão 4.
    """
    C = np.array([0, -18, 8])
    P = np.array([0, 0, 0])
    up = np.array([0, 0, 1])

    # View Matrix
    def normalize(v): return v / np.linalg.norm(v)
    z_c = normalize(C - P)
    u_c = normalize(np.cross(up, z_c))
    v_c = np.cross(z_c, u_c)
    
    V = np.array([
        [u_c[0], u_c[1], u_c[2], -np.dot(u_c, C)],
        [v_c[0], v_c[1], v_c[2], -np.dot(v_c, C)],
        [z_c[0], z_c[1], z_c[2], -np.dot(z_c, C)],
        [0, 0, 0, 1]
    ])

    scene_world = get_solids()
    projected_faces = []

    for name, (verts, faces) in scene_world.items():
        v_cam = apply_transformation(verts, V)
        
        # Projeção Perspectiva Simples
        focal = 1.0 
        v_2d = []
        for x, y, z in v_cam:
            if z <= 0.1: z = 0.1
            v_2d.append([focal * x / z, focal * y / z])
        v_2d = np.array(v_2d)
        
        # Define cor baseada no objeto (valor inteiro para a matriz)
        if name == "cubo": color = 1
        elif name == "hermite": color = 2
        else: color = 3 # toro
        
        projected_faces.append((v_2d, faces, color))
        
    return projected_faces

# ==========================================
# 3. RASTERIZAÇÃO EM MÚLTIPLAS RESOLUÇÕES (Questão 5)
# ==========================================
def rasterize_scene_at_resolution(width, height, scene_data):
    # Buffer de Imagem (Zeros = Fundo Preto)
    buffer = np.zeros((height, width))
    
    # Precisamos escalar os dados normalizados para caber na tela (Viewport Transform)
    # Vamos achar o bounding box global da cena para centralizar
    all_coords = []
    for v_2d, _, _ in scene_data:
        all_coords.append(v_2d)
    all_coords = np.vstack(all_coords)
    
    min_x, max_x = all_coords[:, 0].min(), all_coords[:, 0].max()
    min_y, max_y = all_coords[:, 1].min(), all_coords[:, 1].max()
    
    scale_x = (width * 0.8) / (max_x - min_x)
    scale_y = (height * 0.8) / (max_y - min_y)
    scale = min(scale_x, scale_y) # Manter aspect ratio
    
    # Translação para o centro da tela
    center_x, center_y = width / 2, height / 2
    mid_scene_x = (min_x + max_x) / 2
    mid_scene_y = (min_y + max_y) / 2

    # Ordenar polígonos por profundidade (Algoritmo do Pintor simplificado)
    # Idealmente usaríamos Z-Buffer, mas aqui vamos pela ordem de desenho
    
    for v_2d, faces, color in scene_data:
        # Transforma vértices para coordenadas de Tela (Inteiros)
        screen_verts = (v_2d - [mid_scene_x, mid_scene_y]) * scale + [center_x, center_y]
        
        for face in faces:
            poly_pts = screen_verts[face]
            scanline_fill(poly_pts, buffer, color)
            
    return buffer

def main_q5():
    scene_data = get_projected_scene()
    
    # 3 Resoluções diferentes como pedido
    resolutions = [
        (50, 50),     # Baixa Resolução (Pixel Art)
        (200, 200),   # Média
        (800, 800)    # Alta
    ]
    
    plt.figure(figsize=(15, 5))
    
    for i, (w, h) in enumerate(resolutions):
        print(f"Rasterizando resolução {w}x{h}...")
        img = rasterize_scene_at_resolution(w, h, scene_data)
        
        ax = plt.subplot(1, 3, i + 1)
        # imshow exibe a matriz como imagem. origin='lower' coloca o (0,0) embaixo
        ax.imshow(img, cmap='nipy_spectral', origin='lower', interpolation='nearest')
        ax.set_title(f"Resolução: {w}x{h}")
        ax.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main_q5()