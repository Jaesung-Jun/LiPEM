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
import bone

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
        
        self.model = self.__load(path)
        self.model_bone = self.__bone_load(path)

        if self.model_bone == []:
            print("Bone list empty.")
        
        if not self.model:
            print('Fail to load.')
            return
        print("Load complete : {0}".format(path))

    def __load(self, path):

        print("Loading....")

        if path.lower().endswith(".mqo"):
            model=pymeshio.mqo.reader.read_from_file(path)
            if not model:
                return
            return xbuilder.build(path, model)

        elif path.lower().endswith(".pmd"):
            model=pymeshio.pmd.reader.read_from_file(path)
            if not model:
                return
            return xbuilder.build(path, model)

        elif path.lower().endswith(".pmx"):
            model=pymeshio.pmx.reader.read_from_file(path)
            if not model:
                return
            return pmxbuilder.build(path, model)

        elif path.lower().endswith(".x"):
            model=pymeshio.x.reader.read_from_file(path)
            if not model:
                return
            return xbuilder.build(path, model)
        else:
            print("Unknown file format : {0}".format(path))

    def __bone_load(self, path):

        if path.lower().endswith(".pmd"):
            model=pymeshio.pmd.reader.read_from_file(path)
            if not model:
                return

        elif path.lower().endswith(".pmx"):
            model=pymeshio.pmx.reader.read_from_file(path)
            if not model:
                return

        else:
            print("Unknown file format : {0}".format(path))
            return
        
        bone_temp = []
        main_bone_position = []

        for i in range(len(model.bones)):
            if model.bones[i].name in bone.main_bone_info():
                print("{0} : {1}".format(model.bones[i].name, str(model.bones[i].position)))
                bone_temp.append(model.bones[i].name)
                main_bone_position.append(model.bones[i].position)

        if len(bone_temp) - len(bone.main_bone_info()) != 0:
            print("can't find : {0}".format(list(set(bone.main_bone_info()) - set(bone_temp))))

        return main_bone_position

    def draw(self):
        self.model.draw()

    def draw_bone(self):
        glDepthFunc(GL_ALWAYS)
        glColor3f(0, 0, 1)
        glPointSize(7.0)
        for i in range(len(self.model_bone)):
            glBegin(GL_POINTS)
            glVertex3f(self.model_bone[i].x, self.model_bone[i].y, self.model_bone[i].z)
            glEnd()
        glDepthFunc(GL_LESS)

def main(display=(DISPLAY_X, DISPLAY_Y)):
        
    cameraxyz = [0, 10, 3]
    objectxyz = [0, 10, 0]
    upxyz = [0, 1, 0]

    path = "miku/miku.pmx"
    model_load = Model_Load(path)
    scene_load = Scene()
    grid_load = opengl.drawgrid.Grid(100)
    
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)

    glClearColor(150, 150, 150, 0)
    

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
                elif event.key == pg.K_UP: cameraxyz[1] -= 3
                elif event.key == pg.K_DOWN: cameraxyz[1] -= -3
                elif event.key == pg.K_RIGHT: cameraxyz[0] -= 3
                elif event.key == pg.K_LEFT:  cameraxyz[0] -= -3
                elif event.key == pg.K_d: upxyz[0] -= -0.4
                elif event.key == pg.K_a: upxyz[0] -= 0.4
                elif event.key == pg.K_w: upxyz[1] -= -0.4
                elif event.key == pg.K_s: upxyz[1] -= 0.4
                """
                elif event.key == pg.K_2: cameraxyz[2] += 0.1
                elif event.key == pg.K_1: 
                    cameraxyz[2] += -0.1
                    if cameraxyz[2] < 0.1:
                        cameraxyz[2] = 0.1
                """
        """
        if ry > 0:
            ry -= 3
        else:
            ry = 360
        """
        
        glLoadIdentity()
        gluPerspective(60.0, DISPLAY_X/DISPLAY_Y, 10, 10)
        glScalef(0.1, 0.1, 0.1)
        #glRotatef(ry, 0, 1, 0)
        #glRotatef(rx, 1, 0, 0)
        #glTranslatef(tx, ty, tz)
        gluLookAt(cameraxyz[0], cameraxyz[1], cameraxyz[2],
                  objectxyz[0], objectxyz[1], objectxyz[2],
                  upxyz[0], upxyz[1], upxyz[2])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        model_load.draw()
        model_load.draw_bone()
        scene_load.draw()
        grid_load.draw()

        pg.display.flip()
        clock.tick(30)
        
if __name__ == "__main__":
    main()

