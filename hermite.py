import math
import matplotlib.pyplot as plt # Apenas para visualização final

# ==========================================
# 1. Mini-Engine de Matemática (Sem Numpy)
# ==========================================

def vec_add(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]

def vec_sub(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]

def vec_mul(v, scalar):
    return [v[0]*scalar, v[1]*scalar, v[2]*scalar]

def vec_dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def vec_cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def vec_len(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def vec_norm(v):
    l = vec_len(v)
    if l == 0: return [0, 0, 0]
    return [v[0]/l, v[1]/l, v[2]/l]

def mat_mul_vec(matrix_4x4, vec_4):
    """Multiplica uma matriz 4x4 por um vetor de tamanho 4."""
    result = [0.0] * 4
    for i in range(4):
        soma = 0
        for j in range(4):
            soma += matrix_4x4[i][j] * vec_4[j]
        result[i] = soma
    return result

# ==========================================
# 2. Lógica da Curva de Hermite
# ==========================================

def hermite_point(t, P0, P1, T0, T1):
    """
    Calcula um ponto na curva usando a forma matricial:
    P(t) = T * M * G
    """
    # Vetor T = [t^3, t^2, t, 1]
    T_vec = [t**3, t**2, t, 1]

    # Matriz de base de Hermite (Transposta para alinhar com P0, P1, T0, T1)
    # Nota: A ordem aqui assume o vetor geometria G = [P0, P1, T0, T1]
    # Coeficientes padrão expandidos:
    # h1(P0) =  2t^3 - 3t^2 + 1
    # h2(P1) = -2t^3 + 3t^2
    # h3(T0) =   t^3 - 2t^2 + t
    # h4(T1) =   t^3 -  t^2
    
    # Vamos calcular manualmente a combinação linear para simplificar
    # sem criar uma estrutura de tensor complexa para xyz
    
    h1 =  2*(t**3) - 3*(t**2) + 1
    h2 = -2*(t**3) + 3*(t**2)
    h3 =    (t**3) - 2*(t**2) + t
    h4 =    (t**3) -    (t**2)
    
    # P(t) = h1*P0 + h2*P1 + h3*T0 + h4*T1
    term1 = vec_mul(P0, h1)
    term2 = vec_mul(P1, h2)
    term3 = vec_mul(T0, h3)
    term4 = vec_mul(T1, h4)
    
    res = vec_add(term1, term2)
    res = vec_add(res, term3)
    res = vec_add(res, term4)
    return res

def hermite_tangent(t, P0, P1, T0, T1):
    """
    Derivada da curva de Hermite para achar a direção (tangente).
    P'(t)
    """
    # Derivadas dos coeficientes:
    # d_h1 =  6t^2 - 6t
    # d_h2 = -6t^2 + 6t
    # d_h3 =  3t^2 - 4t + 1
    # d_h4 =  3t^2 - 2t
    
    dh1 =  6*(t**2) - 6*t
    dh2 = -6*(t**2) + 6*t
    dh3 =  3*(t**2) - 4*t + 1
    dh4 =  3*(t**2) - 2*t
    
    term1 = vec_mul(P0, dh1)
    term2 = vec_mul(P1, dh2)
    term3 = vec_mul(T0, dh3)
    term4 = vec_mul(T1, dh4)
    
    res = vec_add(term1, term2)
    res = vec_add(res, term3)
    res = vec_add(res, term4)
    return vec_norm(res) # Retorna normalizado

# ==========================================
# 3. Geração do Cano (Sweep)
# ==========================================

def generate_hermite_pipe(P0, P1, T0, T1, radius, steps=50, resolution=12):
    vertices = []
    faces = []
    rings = [] # Guarda índices dos vértices de cada anel

    # Vetor "Up" global arbitrário para iniciar o frame
    global_up = [0, 0, 1]

    for i in range(steps + 1):
        t = i / float(steps)
        
        # 1. Obter posição central e vetor direção (tangente)
        center = hermite_point(t, P0, P1, T0, T1)
        tangent = hermite_tangent(t, P0, P1, T0, T1)
        
        # 2. Criar Base Ortonormal (Frame Local)
        # Vetor Right = Cross(Tangent, Up)
        right = vec_cross(tangent, global_up)
        
        # Se tangente for paralela ao Up, muda o Up temporariamente
        if vec_len(right) < 0.001:
            right = vec_cross(tangent, [1, 0, 0])
            
        right = vec_norm(right)
        
        # Vetor Up Local (Real) = Cross(Right, Tangent)
        up_local = vec_cross(right, tangent)
        up_local = vec_norm(up_local)
        
        # 3. Gerar vértices do círculo (Anel)
        current_ring_indices = []
        for j in range(resolution):
            angle = 2 * math.pi * j / resolution
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            # Ponto = Centro + (Right * cos * r) + (Up * sin * r)
            r_vec = vec_mul(right, cos_a * radius)
            u_vec = vec_mul(up_local, sin_a * radius)
            
            offset = vec_add(r_vec, u_vec)
            vertex = vec_add(center, offset)
            
            vertices.append(vertex)
            current_ring_indices.append(len(vertices) - 1)
        
        rings.append(current_ring_indices)

    # 4. Criar Faces (Triângulos) conectando os anéis
    for i in range(len(rings) - 1):
        ring_current = rings[i]
        ring_next = rings[i+1]
        
        for j in range(resolution):
            # Índices
            idx0 = ring_current[j]
            idx1 = ring_current[(j + 1) % resolution]
            idx2 = ring_next[j]
            idx3 = ring_next[(j + 1) % resolution]
            
            # Dois triângulos para formar o quad
            faces.append([idx0, idx1, idx2])
            faces.append([idx1, idx3, idx2])
            
    return vertices, faces

# ==========================================
# 4. Execução e Visualização
# ==========================================

# Definição da Curva de Hermite
p_start = [0, 0, 0]
p_end   = [10, 10, 5]
t_start = [0, 20, 0]   # Tangente inicial forte em Y
t_end   = [20, 0, 0]   # Tangente final forte em X
raio = 1.0

# Gera a malha (Só usa listas e math)
verts, tris = generate_hermite_pipe(p_start, p_end, t_start, t_end, raio)

print(f"Gerado: {len(verts)} vértices e {len(tris)} faces.")

# --- Plotagem (Requer Matplotlib apenas para exibir, o cálculo já foi feito) ---
# Precisamos converter as listas de volta para o formato que o plot_trisurf aceita
# Se você não tiver matplotlib, pode pular esta parte e salvar num arquivo .obj

try:
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Separar X, Y, Z em listas simples
    vx = [v[0] for v in verts]
    vy = [v[1] for v in verts]
    vz = [v[2] for v in verts]

    ax.plot_trisurf(vx, vy, vz, triangles=tris, cmap='magma', edgecolor='none', alpha=0.9)

    # Plotar o "esqueleto" da curva para comparação
    curve_line_x = []
    curve_line_y = []
    curve_line_z = []
    for i in range(51):
        t = i/50
        p = hermite_point(t, p_start, p_end, t_start, t_end)
        curve_line_x.append(p[0])
        curve_line_y.append(p[1])
        curve_line_z.append(p[2])
    
    ax.plot(curve_line_x, curve_line_y, curve_line_z, 'w--', linewidth=2, label="Espinha (Hermite)")

    ax.set_title("Cano de Hermite (Cálculo Puro Python)")
    ax.legend()
    # Ajustar proporção visual
    max_range = max(max(vx)-min(vx), max(vy)-min(vy), max(vz)-min(vz)) / 2.0
    mid_x = (max(vx)+min(vx)) * 0.5
    mid_y = (max(vy)+min(vy)) * 0.5
    mid_z = (max(vz)+min(vz)) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    plt.show()

except NameError:
    print("Matplotlib não encontrado, mas os vértices foram calculados com sucesso.")