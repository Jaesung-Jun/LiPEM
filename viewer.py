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
import xbuilder
import pmdbuilder
import mqobuilder

import os
import numpy as np
import pygame as pg
import opengl
import bone
import math

import animation.main

from estimater import Get_Pose_From_Webcam

DISPLAY_X = 1280
DISPLAY_Y = 720
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
        """
        elif path.lower().endswith(".mqo"):
            model=pymeshio.mqo.reader.read_from_file(path)
            if not model:
                return
            return mqobuilder.build(path, model)

        elif path.lower().endswith(".x"):
            model=pymeshio.x.reader.read_from_file(path)
            if not model:
                return
            return xbuilder.build(path, model)
        """
            
        if path.lower().endswith(".pmd"):
            model=pymeshio.pmd.reader.read_from_file(path)
            if not model:
                return
            return pmdbuilder.build(path, model)
        
        elif path.lower().endswith(".pmx"):
            model=pymeshio.pmx.reader.read_from_file(path)
            if not model:
                return
            return pmxbuilder.build(path, model)

        else:
            print("Unknown file format : {0}".format(path))


    def __bone_load(self, path):

        if path.lower().endswith(".pmd"):
            model=pymeshio.pmd.reader.read_from_file(path)
            animation.main.Animation(model)
            if not model:
                return

        elif path.lower().endswith(".pmx"):
            model=pymeshio.pmx.reader.read_from_file(path)
            animation.main.Animation(model)
            if not model:
                return

        else:
            print("Unknown file format : {0}".format(path))
            return
        
        bone_temp = []
        main_bone_position = {}

        for i in range(len(model.bones)):
            if model.bones[i].name in bone.main_bone_info():
                print("{0} : {1}".format(model.bones[i].name, str(model.bones[i].position)))
                bone_temp.append(model.bones[i].name)
                #main_bone_position.append(model.bones[i].position)
                main_bone_position[model.bones[i].name] = model.bones[i].position

        if len(bone_temp) - len(bone.main_bone_info()) != 0:
            print("can't find : {0}".format(list(set(bone.main_bone_info()) - set(bone_temp))))

        return main_bone_position

    def draw(self):
        self.model.draw()

    def draw_bone(self):
        glDepthFunc(GL_ALWAYS)
        glColor3f(1, 0, 0)
        glPointSize(7.0)
        glLineWidth(3.0)
        #for i in range(len(self.model_bone)):
        #    glVertex3f(self.model_bone[i].x, self.model_bone[i].y, self.model_bone[i].z)
        glBegin(GL_LINE_STRIP)
        glVertex3f(self.model_bone[bone.HEAD].x, self.model_bone[bone.HEAD].y, self.model_bone[bone.HEAD].z)
        glVertex3f(self.model_bone[bone.LEFT_ARM].x, self.model_bone[bone.LEFT_ARM].y, self.model_bone[bone.LEFT_ARM].z)
        glVertex3f(self.model_bone[bone.LEFT_ELBOW].x, self.model_bone[bone.LEFT_ELBOW].y, self.model_bone[bone.LEFT_ELBOW].z)
        glVertex3f(self.model_bone[bone.LEFT_WRIST].x, self.model_bone[bone.LEFT_WRIST].y, self.model_bone[bone.LEFT_WRIST].z)
        glEnd()

        glBegin(GL_LINE_STRIP)
        glVertex3f(self.model_bone[bone.HEAD].x, self.model_bone[bone.HEAD].y, self.model_bone[bone.HEAD].z)
        glVertex3f(self.model_bone[bone.LEFT_FOOT].x, self.model_bone[bone.LEFT_FOOT].y, self.model_bone[bone.LEFT_FOOT].z)
        glVertex3f(self.model_bone[bone.LEFT_KNEE].x, self.model_bone[bone.LEFT_KNEE].y, self.model_bone[bone.LEFT_KNEE].z)
        glVertex3f(self.model_bone[bone.LEFT_ANKLE].x, self.model_bone[bone.LEFT_ANKLE].y, self.model_bone[bone.LEFT_ANKLE].z)
        glEnd()

        glBegin(GL_LINE_STRIP)
        glVertex3f(self.model_bone[bone.HEAD].x, self.model_bone[bone.HEAD].y, self.model_bone[bone.HEAD].z)
        glVertex3f(self.model_bone[bone.RIGHT_ARM].x, self.model_bone[bone.RIGHT_ARM].y, self.model_bone[bone.RIGHT_ARM].z)
        glVertex3f(self.model_bone[bone.RIGHT_ELBOW].x, self.model_bone[bone.RIGHT_ELBOW].y, self.model_bone[bone.RIGHT_ELBOW].z)
        glVertex3f(self.model_bone[bone.RIGHT_WRIST].x, self.model_bone[bone.RIGHT_WRIST].y, self.model_bone[bone.RIGHT_WRIST].z)
        glEnd()

        glBegin(GL_LINE_STRIP)
        glVertex3f(self.model_bone[bone.HEAD].x, self.model_bone[bone.HEAD].y, self.model_bone[bone.HEAD].z)
        glVertex3f(self.model_bone[bone.RIGHT_FOOT].x, self.model_bone[bone.RIGHT_FOOT].y, self.model_bone[bone.RIGHT_FOOT].z)
        glVertex3f(self.model_bone[bone.RIGHT_KNEE].x, self.model_bone[bone.RIGHT_KNEE].y, self.model_bone[bone.RIGHT_KNEE].z)
        glVertex3f(self.model_bone[bone.RIGHT_ANKLE].x, self.model_bone[bone.RIGHT_ANKLE].y, self.model_bone[bone.RIGHT_ANKLE].z)
        glEnd()
        
        glDepthFunc(GL_LESS)

class Draw_Estimated_Bone:

    def __init__(self, estimated_bone_info):
        if len(estimated_bone_info) != 0:
            for i in range(len(estimated_bone_info[0])):
                estimated_bone_info[0][i][0] += -30
                estimated_bone_info[0][i][2] += -115
                estimated_bone_info[0][i][1] += 250
            self.estimated_bone_info = estimated_bone_info

    def draw_point(self):
        if len(self.estimated_bone_info) != 0:
            glBegin(GL_POINTS)
            for i in range(len(self.estimated_bone_info[0])):
                glVertex3f(self.estimated_bone_info[0][i][0], self.estimated_bone_info[0][i][2], self.estimated_bone_info[0][i][1])
            glEnd()
            
    def draw_line(self):
        if len(self.estimated_bone_info) != 0:
            glDepthFunc(GL_ALWAYS)
            glColor3f(1, 0, 0)
            glPointSize(7.0)
            glLineWidth(3.0)

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][0][0], self.estimated_bone_info[0][0][2], self.estimated_bone_info[0][0][1])        #core - upper body
            glVertex3f(self.estimated_bone_info[0][2][0], self.estimated_bone_info[0][2][2], self.estimated_bone_info[0][2][1])        #core - hip
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][0][0], self.estimated_bone_info[0][0][2], self.estimated_bone_info[0][0][1])        #core - upper body
            glVertex3f(self.estimated_bone_info[0][1][0], self.estimated_bone_info[0][1][2], self.estimated_bone_info[0][1][1])        #core - hip
            glEnd()
            ########################################################################################################
            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][0][0], self.estimated_bone_info[0][0][2], self.estimated_bone_info[0][0][1])        #core - upper body
            glVertex3f(self.estimated_bone_info[0][3][0], self.estimated_bone_info[0][3][2], self.estimated_bone_info[0][3][1])        #l_sho
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][0][0], self.estimated_bone_info[0][0][2], self.estimated_bone_info[0][0][1])        #core - upper body
            glVertex3f(self.estimated_bone_info[0][9][0], self.estimated_bone_info[0][9][2], self.estimated_bone_info[0][9][1])        #r_sho
            glEnd()
            ########################################################################################################
            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][2][0], self.estimated_bone_info[0][2][2], self.estimated_bone_info[0][2][1])        #core - hip
            glVertex3f(self.estimated_bone_info[0][6][0], self.estimated_bone_info[0][6][2], self.estimated_bone_info[0][6][1])        #l_hip
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][2][0], self.estimated_bone_info[0][2][2], self.estimated_bone_info[0][2][1])        #core - hip
            glVertex3f(self.estimated_bone_info[0][12][0], self.estimated_bone_info[0][12][2], self.estimated_bone_info[0][12][1])        #r_hip
            glEnd()
            ########################################################################################################
            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][1][0], self.estimated_bone_info[0][1][2], self.estimated_bone_info[0][1][1])        #nose
            glVertex3f(self.estimated_bone_info[0][15][0], self.estimated_bone_info[0][15][2], self.estimated_bone_info[0][15][1])        #right eye
            glVertex3f(self.estimated_bone_info[0][17][0], self.estimated_bone_info[0][17][2], self.estimated_bone_info[0][17][1])        #right ear
            glEnd()
            
            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][1][0], self.estimated_bone_info[0][1][2], self.estimated_bone_info[0][1][1])        #nose
            glVertex3f(self.estimated_bone_info[0][16][0], self.estimated_bone_info[0][16][2], self.estimated_bone_info[0][16][1])        #left eye
            glVertex3f(self.estimated_bone_info[0][18][0], self.estimated_bone_info[0][18][2], self.estimated_bone_info[0][18][1])        #left ear
            glEnd()

            ########################################################################################################


            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][3][0], self.estimated_bone_info[0][3][2], self.estimated_bone_info[0][3][1])        # l_sho
            glVertex3f(self.estimated_bone_info[0][4][0], self.estimated_bone_info[0][4][2], self.estimated_bone_info[0][4][1])        # l_elb
            glVertex3f(self.estimated_bone_info[0][5][0], self.estimated_bone_info[0][5][2], self.estimated_bone_info[0][5][1])        # l_wri
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][6][0], self.estimated_bone_info[0][6][2], self.estimated_bone_info[0][6][1])        # l_hip
            glVertex3f(self.estimated_bone_info[0][7][0], self.estimated_bone_info[0][7][2], self.estimated_bone_info[0][7][1])        # l_knee
            glVertex3f(self.estimated_bone_info[0][8][0], self.estimated_bone_info[0][8][2], self.estimated_bone_info[0][8][1])        # l_ank
            glEnd()

            ########################################################################################################

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][9][0], self.estimated_bone_info[0][9][2], self.estimated_bone_info[0][9][1])        # r_sho
            glVertex3f(self.estimated_bone_info[0][10][0], self.estimated_bone_info[0][10][2], self.estimated_bone_info[0][10][1])        # r_elb
            glVertex3f(self.estimated_bone_info[0][11][0], self.estimated_bone_info[0][11][2], self.estimated_bone_info[0][11][1])        # r_wri
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex3f(self.estimated_bone_info[0][12][0], self.estimated_bone_info[0][12][2], self.estimated_bone_info[0][12][1])        # r_hip
            glVertex3f(self.estimated_bone_info[0][13][0], self.estimated_bone_info[0][13][2], self.estimated_bone_info[0][13][1])        # r_knee
            glVertex3f(self.estimated_bone_info[0][14][0], self.estimated_bone_info[0][14][2], self.estimated_bone_info[0][14][1])        # r_ank
            glEnd()

            glDepthFunc(GL_LESS)

class Draw_Joint:

    def __init__(self, _main_bone_position):        
        # Arguments
        #
        # main_bone_position : Dictionary
        #
        # ex) {"HEAD":[0, 0, 0], ...... }

        self.main_bone_position = _main_bone_position

        if len(bone_temp) - len(bone.main_bone_info()) != 0:
            print("can't find : {0}".format(list(set(bone.main_bone_info()) - set(bone_temp))))


def main(display=(DISPLAY_X, DISPLAY_Y)):
        
    camera_pos  = np.array([0.0, 10.0, 3.0])
    lookat_pos = np.array([0.0, 10.0, 0.0])
    camera_up = np.array([0.0, 1.0, 0.0])
    aspect = display[0]/display[1]
    zoom = 10.0

    path = "models/Ashe/Ashe.pmx"
    model_load = Model_Load(path)
    scene_load = Scene()
    grid_load = opengl.drawgrid.Grid(100)
    
    pg.init()
    pg.display.set_caption('LiPEM (Light Pose Estimation with 3D Models)')
    
    #Texts on window
    text_font = pg.font.SysFont("Arial", 15)

    clock = pg.time.Clock()
    screen = pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)

    glClearColor(150, 150, 150, 0)
    #View
    glViewport(0, 0, display[0], display[1])

    glEnable(GL_DEPTH_TEST)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0,1.0)

    pose = Get_Pose_From_Webcam()
    estimated_bone_info = []

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                elif event.key == pg.K_UP:
                    camera_pos[1] += 0.3
                elif event.key == pg.K_DOWN: 
                    camera_pos[1] -= 0.3
                elif event.key == pg.K_RIGHT: 
                    camera_pos[0] += 0.3
                elif event.key == pg.K_LEFT:  
                    camera_pos[0] -= 0.3
                elif event.key == pg.K_2: 
                    zoom += 0.3
                elif event.key == pg.K_1: 
                    zoom += -0.3
                    if zoom < 0:
                        zoom = 0.1
                elif event.key == pg.K_d:
                    lookat_pos[0] -= -0.3
                    camera_pos[0] -= -0.3
                elif event.key == pg.K_a: 
                    lookat_pos[0] -= 0.3
                    camera_pos[0] -= 0.3
                elif event.key == pg.K_w: 
                    lookat_pos[1] -= -0.3
                    camera_pos[1] -= -0.3
                elif event.key == pg.K_s: 
                    lookat_pos[1] -= 0.3
                    camera_pos[1] -= 0.3
                print("camera pos : {}, zoom : {}".format(camera_pos, zoom))

        """
        pos_text = text_font.render('camera position : {0}, {1}, {2}'.format(camera_pos[0], camera_pos[1], camera_pos[2]), True, (0, 0, 0))
        zoom_text = text_font.render('zoom position : {}'.format(zoom), True, (0, 0, 0))
        screen.blit(pos_text, (0, 0))
        screen.blit(pos_text, (0, 20))
        """
        
        glLoadIdentity()
        glOrtho(-aspect*zoom, aspect*zoom, -1*zoom, 1*zoom, -5*zoom, 50*zoom);
        glMatrixMode(GL_MODELVIEW)
        #glRotatef(ry, 0, 1, 0)
        #glRotatef(rx, 1, 0, 0)
        #glTranslatef(tx, ty, tz)
        glScalef(1, 1, 1)
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  lookat_pos[0], lookat_pos[1], lookat_pos[2],
                  camera_up[0], camera_up[1], camera_up[2])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        model_load.draw()
        model_load.draw_bone()
        scene_load.draw()
        grid_load.draw()

        estimated_bone_info = pose.estimate_poses()
        estimated_bone = Draw_Estimated_Bone(estimated_bone_info)

        #if estimated_bone_info != None:
        
        glColor3f(0, 1, 0)
        
        if len(estimated_bone_info) != 0:
            estimated_bone.draw_point()
        if len(estimated_bone_info) != 0:
            estimated_bone.draw_line()
        pg.display.flip()
        clock.tick(30)
        
if __name__ == "__main__":
    main()
