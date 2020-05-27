import pygame

class sonic():
    '''
    posicion -> tupla (x,y)
    
    radio -> entero
    
    nombre -> cadena
    '''
    def __init__(self, window, pos, nombre, time_on=5, c_on=(214,43,6), c_off=(0,139,139), size=8):
        self.x = pos[0]
        self.y = pos[1]
        self.name = nombre
        self.window = window
        self.radius = size
        self.timer=0
        self.timer0=None
        self.status=False
        self.congelado=False
        self.time_on=time_on
        self.on = c_on
        self.off = c_off

    def collide(self, status):
        self.status=status
        if self.status==True:
            self.timer0 = self.timer
        else:
            if self.timer0 is not None:
                if self.timer-self.timer0<self.time_on:
                    pygame.draw.circle(self.window, self.on, (self.x, self.y), self.radius)
                else:
                    pygame.draw.circle(self.window, self.off, (self.x, self.y), self.radius)
            else:
                pygame.draw.circle(self.window, self.off, (self.x, self.y), self.radius)
            self.timer+=1
        
    def freeze(self, STATE):
        if STATE==True:
            self.congelado=True
        else:
            self.congelado=False
        
    def state(self):
        if self.status==True:
            devolver = {'nombre':self.name,'status':self.status, 'pos':(self.x, self.y), 'time':self.timer0}
        else:
            devolver={'nombre':self.name,'status':self.status, 'pos':(self.x, self.y), 'time':None}
        return devolver

def triangular(tiempos_activacion, speed=10):
    '''Lista de listas:
        
    [[nombre1, status, position, time],
     [nombre2, status, position, time],
     [nombre3, status, position, time]]
    
    speed es la velocidad de desplazamiento de la onda
    '''
    # import math
    #implementar comprobacion de distancia l
    # import numpy as np
    ndic=sorted(tiempos_activacion, key=lambda k:k[3])
    tiempos=[i[3] for i in ndic]
    num_sensores=len(tiempos)
    if tiempos.count(tiempos[0])==num_sensores:
        return tiempos_iguales(tiempos_activacion)
    else:
        dt=[]
        for i in range(1, len(tiempos)):
            dt.append(tiempos[i]-tiempos[i-1])
        d1 = speed*dt[0]
        d2 = speed*dt[1]
        print(f'\t\tdt1:{d1}\tdt2:{d2}')
        if d1==0 and d2==0:
            print('Error. Tiempos iguales')
            return None
        else:
            l=250           #distancia entre sensores
            distance = (((l**2-d1**2)+(l**2-d2**2))/(2*(d1+d2)))/2   #al sensor del centro
            # theta = math.pi/2-theta1/2+theta2/2
            print(f'La distancia es: {distance}')
            return int(distance)

def tiempos_iguales(t_ACTIV):
    if len(t_ACTIV)==3:
        ax = t_ACTIV[0][2][0]
        ay = t_ACTIV[0][2][1]
        bx = t_ACTIV[1][2][0]
        by = t_ACTIV[1][2][1]
        cx = t_ACTIV[2][2][0]
        cy = t_ACTIV[2][2][1]
        aa = ax**2+ay**2
        bb = bx**2+by**2
        cc = cx**2+cy**2
        D__1 = 1/(2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by)))
        Ux = D__1*(aa*(by-cy)+bb*(cy-ay)+cc*(ay-by))
        Uy = D__1*(aa*(cx-bx)+bb*(ax-cx)+cc*(bx-ax))
        # distance = np.sqrt(Ux**2+Uy**2)
        # print(distance)
        return (int(Ux), int(Uy))
    else:
        print('Mas de tres sensores!')
        return None

def color_esc(color='Crimson', allcolors=False):
    '''No importan las mayusculas
    
    BLACK, GRAY, SALMON, RED, LIME, BLUE, CRIMSON, LIGHTBLUE, HOTPINK, TOMATO, ORANGE, YELLOW,
    INDIGO, DARKMAGENTA, GREEN, MEDIUMSPRINGGREEN, DARKCYAN, CYAN, TURQOISE, DODGERBLUE, BROWN,
    SILVER, SLATEGRAY, DARKSLATEGRAY'''
    dicc={"BLACK": (0, 0, 0), "GRAY": (128, 128, 128), "SALMON": (250, 128, 114),
          "RED": (255, 0, 0), "LIME": (0, 255, 0), "BLUE": (0, 0, 255), 
          "CRIMSON": (214, 43, 6), "LIGHTBLUE": (6, 197, 214), "HOTPINK": (255, 105, 180),
          "TOMATO": (255, 99, 71), "ORANGE": (255, 165, 0), "YELLOW": (255, 255, 0),
          "INDIGO": (75, 0, 130), "DARKMAGENTA": (139, 0, 139), "GREEN": (0, 128, 0),
          "MEDIUMSPRINGGREEN": (0, 250, 114), "DARKCYAN": (0, 139, 139), "CYAN": (0, 255, 255),
          "TURQOISE": (64, 224, 208), "DODGERBLUE": (30, 144, 155), "BROWN": (165, 42, 42),
          "SILVER": (192, 192, 192), "SLATEGRAY": (112, 128, 144), "DARKSLATEGRAY": (47, 79, 79)}
    color = color.upper()
    if allcolors==True:
        return dicc
    else:
        if color in dicc:
            return dicc[color]
        else:
             print('No hay el color escogido. Se devolvera por defecto el Crimson')
             return dicc['CRIMSON']
         
