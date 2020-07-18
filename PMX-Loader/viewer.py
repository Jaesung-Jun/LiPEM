import pymeshio.pmx.reader
import pymeshio
import opengl.material
import opengl.texture
import opengl.vertexarray
import opengl.coord
import opengl.drawgrid

from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.GLU import *

import pmxbuilder
import os
import numpy as np
import pygame as pg
import opengl

DISPLAY_X = 1280
DISPLAY_Y = 760
VIEWPORT_X = 3
VIEWPORT_Y = 3

class Scene:

    def __init__(self, items=[]):
        """
        items : pmx(or pmd etc.)builder.build() Instance
        """
        self.items = items
        self.coord=opengl.coord.Coord(100)

    def draw(self):
        self.coord.draw()
        for item in self.items: item.draw()

class Model_Load:

    def __init__(self, path):
        self.model = pmxbuilder.build(path)
        if not self.model:
            print('fail to load')
            return
        print(self.model)

    def draw(self):
        self.model.draw()

def main(display=(DISPLAY_X, DISPLAY_Y)):
        
    tx = 0
    ty = -10
    tz = 0
    rx = 0
    ry = 180
    zoom = 0.1

    path = "miku/miku.pmx"
    model_load = Model_Load(path)
    scene_load = Scene()
    grid_load = opengl.drawgrid.Grid(100)
    
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)

    glClearColor(150, 150, 150, 0)
    
    gluPerspective(60.0, DISPLAY_Y/DISPLAY_X, 1.0, 20.0)
    
    #View
    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    aspect = display[0]/display[1]
    glOrtho(-aspect, aspect, -1, 1, -1, 1);
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0,1.0)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                elif event.key == pg.K_UP: rx -= 3
                elif event.key == pg.K_DOWN: rx -= -3
                elif event.key == pg.K_RIGHT: ry -= 3
                elif event.key == pg.K_LEFT:  ry -= -3
                elif event.key == pg.K_d: tx -= -0.4
                elif event.key == pg.K_a: tx -= 0.4
                elif event.key == pg.K_w: ty -= -0.4
                elif event.key == pg.K_s: ty -= 0.4
                elif event.key == pg.K_2: zoom += 0.01
                elif event.key == pg.K_1: 
                    zoom += -0.01
                    if zoom < 0.01:
                        zoom = 0.01
        if ry > 0:
            ry -= 3
        else:
            ry = 360

        glLoadIdentity()

        glScalef(zoom, zoom, zoom)
        glRotatef(ry, 0, 1, 0)
        glRotatef(rx, 1, 0, 0)
        glTranslatef(tx, ty, tz)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        model_load.draw()
        scene_load.draw()
        grid_load.draw()

        pg.display.flip()
        clock.tick(30)
        
if __name__ == "__main__":
    main()

