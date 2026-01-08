import numpy as np

def get_hermite_mesh(P0, P1, T0, T1, radius=0.3, steps=40, resolution=8):
    t = np.linspace(0, 1, steps).reshape(-1, 1)
    
    h1 = 2*t**3 - 3*t**2 + 1
    h2 = -2*t**3 + 3*t**2
    h3 = t**3 - 2*t**2 + t
    h4 = t**3 - t**2
    
    path = h1*P0 + h2*P1 + h3*T0 + h4*T1
    
    dh1 = 6*t**2 - 6*t
    dh2 = -6*t**2 + 6*t
    dh3 = 3*t**2 - 4*t + 1
    dh4 = 3*t**2 - 2*t
    tangents = dh1*P0 + dh2*P1 + dh3*T0 + dh4*T1
    
    vertices = []
    for i in range(steps):
        p, tan = path[i], tangents[i]
        tan /= np.linalg.norm(tan)
        
        # Criar base ortonormal (Frame de Frenet simplificado)
        up = np.array([0,0,1]) if abs(tan[2]) < 0.9 else np.array([1,0,0])
        side = np.cross(tan, up)
        side /= np.linalg.norm(side)
        up_final = np.cross(side, tan)
        
        # Gerar o anel de vértices
        angles = np.linspace(0, 2*np.pi, resolution, endpoint=False)
        for a in angles:
            v = p + radius * (np.cos(a)*side + np.sin(a)*up_final)
            vertices.append(v)
            
    # Faces conectando os anéis
    faces = []
    for i in range(steps - 1):
        for j in range(resolution):
            p0, p1 = i*resolution + j, i*resolution + (j+1)%resolution
            p2, p3 = (i+1)*resolution + (j+1)%resolution, (i+1)*resolution + j
            faces.extend([[p0, p1, p2], [p0, p2, p3]])
            
    return np.array(vertices), faces