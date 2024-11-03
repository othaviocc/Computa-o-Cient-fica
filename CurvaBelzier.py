#TAREFA: Visualização de duas curvas cúbicas de Bézier (usando classes)
#Othavio Christmann Correa   

import math
import numpy as np
import pyxel as px

class CurvaBelzier:
    def __init__(self,p0,p1,p2,p3):
        self.p0 = np.array(p0)
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.p3 = np.array(p3)
        
    def CalculoTangente(self): 
        d0 = -3 * (1 - t) ** 2
        d1 = 3 * (1 - 4 * t + 3 * t ** 2)
        d2 = 3 * (2 * t - t ** 2)
        d3 = 3 * t ** 2
        
        dx = d0 * self.p0[0] + d1 * self.p1[0] + d2 * self.p2[0] + d3 * self.p3[0]
        dy = d0 * self.p0[1] + d1 * self.p1[1] + d2 * self.p2[1] + d3 * self.p3[1]

        x = ((1 - t)**3)*self.p0[0] + (3*t*((1 - t)**2))*self.p1[0] + (3*(t**2)*(1 - t))*self.p2[0] + (t**3)*self.p3[0]
        y = ((1 - t)**3)*self.p0[1] + (3*t*((1 - t)**2))*self.p1[1] + (3*(t**2)*(1 - t))*self.p2[1] + (t**3)*self.p3[1]
        
        px.circ(x, y, 3, 12)

        tam = math.sqrt(dx*dx + dy*dy)
        px.line(x, y, x + 10*dx/tam, y + 10*dy/tam, 4)
        px.line(x, y, x - 10*dy/tam, y + 10*dx/tam, 8)
    
curva1 = CurvaBelzier([400,400],[0,0],[400,0],[1,400])
curva2 = CurvaBelzier([400,400],[400,0],[0,0],[400,0])
curva3 = CurvaBelzier([0,0],[400, 400],[0,400],[400,1])
curva4 = CurvaBelzier([0,0],[0,400],[400,400],[0,400])


def update():
    global t
    t = (px.frame_count / 60) % 1

def draw():
    curva1.CalculoTangente()
    curva2.CalculoTangente() 
    curva3.CalculoTangente()  #oposto a curva1
    curva4.CalculoTangente()  #oposto a curva2


px.init(400, 400)
px.run(update, draw)
