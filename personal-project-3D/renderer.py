from OpenGL.GL import *
from word_builder import build_word_cubes

VERTICES = (
    ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5),
    (-0.5,  0.5, -0.5), (-0.5, -0.5, -0.5),
    ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5),
    (-0.5, -0.5,  0.5), (-0.5,  0.5,  0.5)
)

SURFACES = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

EDGES = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 7), (3, 6)
)

FACE_COLORS = (
    (0.15, 0.35, 0.65),
    (0.20, 0.45, 0.80),
    (0.30, 0.65, 1.00),
    (0.20, 0.45, 0.80),
    (0.45, 0.75, 1.00),
    (0.10, 0.25, 0.50)
)

def draw_cube(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # грани
    glBegin(GL_QUADS)
    for i, surface in enumerate(SURFACES):
        glColor3fv(FACE_COLORS[i])
        for vertex in surface:
            glVertex3fv(VERTICES[vertex])
    glEnd()

    # ребра
    glColor3f(0.05, 0.05, 0.1)
    glLineWidth(1.5)
    glBegin(GL_LINES)
    for edge in EDGES:
        for vertex in edge:
            glVertex3fv(VERTICES[vertex])
    glEnd()

    glPopMatrix()

def draw_word(cubes):
    for x, y, z in cubes:
        draw_cube(x, y, z)

def draw_surname(word):
    cubes = build_word_cubes(word)
    draw_word(cubes)