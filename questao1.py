import numpy as np
import matplotlib.pyplot as plt

from solids.cubo import *
from solids.hermite import *
from solids.torus import *
def plot_cube():

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    verts, edges = create_cubo(edge=3, origin=(1, 1, 1))
    plot_cubo(ax, verts, edges, show_vertices=True)

    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Cubo")
    fig.canvas.manager.set_window_title("Questão 1 - item a)")


    plt.show()

def plot_hermite():

    P1 = [0, 0, 0]
    P2 = [4, 4, 2]
    T1 = [4, 0, 2]
    T2 = [0, 4, 2]

    vertices, edges = create_pipe(
        (P1, P2, T1, T2),
        radius=0.3,
        curve_resolution=25,
        circle_resolution=16
    )

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    plot_pipe(ax, vertices, edges, show_vertices=True)

    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Cano curvado - Hermite")
    fig.canvas.manager.set_window_title("Questão 1 - item b)")

    plt.show()

def plot_toro():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    vertices, edges = create_torus(
        inner_radius=1.5,
        outer_radius=3.0,
        resolution=30,
        origin=(0, 0, 0)
    )

    plot_torus(ax, vertices, edges, show_vertices=False)

    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    fig.canvas.manager.set_window_title("Questão 1 - item c)")

    set_equal_axes(ax, vertices)
    ax.set_box_aspect([1, 1, 1])


    plt.show()

def plot_cube_triangle_mesh():
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        vertices_cubo = [
            (1, 1, 1),
            (4, 1, 1),
            (4, 4, 1),
            (1, 4, 1),
            (1, 1, 4),
            (4, 1, 4),
            (4, 4, 4),
            (1, 4, 4)
        ]

        verts, faces = cube_to_triangle_mesh(vertices_cubo)
        plot_triangle_mesh(ax, verts, faces, color="pink")

        ax.set_box_aspect([1, 1, 1])
        fig.canvas.manager.set_window_title("Questão 1 - item d)")
        ax.set_title("Cubo – Malha Triangular")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        plt.show()

def plot_hermite_pipe_triangle_mesh():

    control_points = [
        (0, 0, 0),   
        (4, 4, 2),   
        (4, 0, 3),   
        (0, 4, 3)    
    ]

    curve_resolution = 20
    circle_resolution = 12

    vertices, _ = create_pipe(
        control_points,
        radius=0.3,
        curve_resolution=curve_resolution,
        circle_resolution=circle_resolution
    )

    verts, faces = pipe_to_triangle_mesh(
        vertices,
        curve_resolution=curve_resolution,
        circle_resolution=circle_resolution
    )

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    plot_triangle_mesh(ax, verts, faces, color="orange")

    ax.set_box_aspect([1, 1, 1])
    fig.canvas.manager.set_window_title("Questão 1 - item d)")
    ax.set_title("Cano Curvado – Malha Triangular (Hermite)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()

def plot_torus_triangle_mesh():

    resolution = 30

    vertices, _ = create_torus(
        inner_radius=1.5,
        outer_radius=3.0,
        resolution=resolution
    )

    verts, faces = torus_to_triangle_mesh(
        vertices,
        resolution_u=resolution,
        resolution_v=resolution
    )

    fig = plt.figure()
    
    fig.canvas.manager.set_window_title("Questão 1 - item d)")
    ax = fig.add_subplot(111, projection="3d")

    plot_triangle_mesh(ax, verts, faces, color="green")

    set_equal_axes(ax, verts)
    ax.set_box_aspect([1, 1, 1])

    ax.set_title("Torus - Malha triangular")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()


def questao_1():

    plot_cube()

    plot_hermite()

    plot_toro()

    plot_cube_triangle_mesh()
    
    plot_hermite_pipe_triangle_mesh()

    plot_torus_triangle_mesh()

if __name__ == "__main__":
    
    dados_objetos = questao_1()
    