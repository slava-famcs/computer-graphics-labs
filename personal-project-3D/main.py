import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from renderer import draw_surname

def main():
    surname = "БАРДАШОВ"

    pygame.init()
    display = (1100, 650)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # буфер глубины
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.08, 0.09, 0.12, 1.0)

    # проекция
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glMatrixMode(GL_MODELVIEW)

    # параметры камеры
    rot_x, rot_y = 15.0, -25.0
    zoom = -42.0
    auto_rotate = True

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom += 2.0
                elif event.button == 5:
                    zoom -= 2.0
            elif event.type == pygame.MOUSEMOTION:
                # вращение при зажатой лкм
                if pygame.mouse.get_pressed()[0]:
                    auto_rotate = False
                    rot_y += event.rel[0] * 0.5
                    rot_x += event.rel[1] * 0.5
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    auto_rotate = not auto_rotate

        if auto_rotate:
            rot_y += 0.6

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0.0, 0.0, zoom)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        draw_surname(surname)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()