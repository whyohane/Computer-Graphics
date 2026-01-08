import numpy as np
from PIL import Image
from questao2 import questao_2_cena_mundo

def orthographic_project(v):
    return np.array([v[0], v[1], v[2]])


COLORS = {
    "cubo": (0, 170, 255),
    "hermite": (255, 160, 60),
    "toro": (0, 200, 120)
}

def rasterize_scene(scene, resolution):
    width, height = resolution
    img = Image.new("RGB", (width, height), "white")
    zbuffer = [[float("inf")] * width for _ in range(height)]

    # Junta todos os pontos 2D
    all_pts = []
    for v, _ in scene.values():
        all_pts.extend(v[:, :2])

    min_x, min_y = np.min(all_pts, axis=0)
    max_x, max_y = np.max(all_pts, axis=0)

    scale = 0.9 * min(
        width / (max_x - min_x),
        height / (max_y - min_y)
    )
    tx = (width - scale * (max_x + min_x)) / 2
    ty = (height - scale * (max_y + min_y)) / 2

    def to_pixel(p):
        x = int(scale * p[0] + tx)
        y = height - int(scale * p[1] + ty)
        return x, y

    def rasterize_triangle(p0, p1, p2, z0, z1, z2, color):
        x0, y0 = to_pixel(p0)
        x1, y1 = to_pixel(p1)
        x2, y2 = to_pixel(p2)

        min_x = max(0, min(x0, x1, x2))
        max_x = min(width - 1, max(x0, x1, x2))
        min_y = max(0, min(y0, y1, y2))
        max_y = min(height - 1, max(y0, y1, y2))

        den = ((y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2))
        if den == 0:
            return

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                u = ((y1 - y2)*(x - x2) + (x2 - x1)*(y - y2)) / den
                v = ((y2 - y0)*(x - x2) + (x0 - x2)*(y - y2)) / den
                w = 1 - u - v
                if u >= 0 and v >= 0 and w >= 0:
                    z = u*z0 + v*z1 + w*z2
                    if z < zbuffer[y][x]:
                        zbuffer[y][x] = z
                        img.putpixel((x, y), color)

    for name, (vertices, faces) in scene.items():
        color = COLORS[name]
        for a, b, c in faces:
            p0, p1, p2 = vertices[a], vertices[b], vertices[c]
            rasterize_triangle(
                p0[:2], p1[:2], p2[:2],
                p0[2], p1[2], p2[2],
                color
            )

    return img

scene = questao_2_cena_mundo()

resolutions = [(32, 32), (64, 64), (128, 128)]

for res in resolutions:
    img = rasterize_scene(scene, res)
    img.save(f"questao5_raster_{res[0]}x{res[1]}.png")
