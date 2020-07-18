from OpenGL.GL import *

class Grid:
    def __init__(self, half_grid_size):

        self.half_grid_size = half_grid_size
    
    def draw(self):

        glBegin(GL_LINES)
        glColor3f(0.75, 0.75, 0.75)
        for i in range(self.half_grid_size):
            
            glVertex3f(i*3, 0, -self.half_grid_size)
            glVertex3f(i*3, 0, self.half_grid_size)
            glVertex3f(-i*3, 0, -self.half_grid_size)
            glVertex3f(-i*3, 0, self.half_grid_size)
            
            glVertex3f(-self.half_grid_size, 0, i*3)
            glVertex3f(self.half_grid_size, 0, i*3)
            glVertex3f(-self.half_grid_size, 0, -i*3)
            glVertex3f(self.half_grid_size, 0, -i*3)

        glEnd()
