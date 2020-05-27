import pygame, sys
import numpy as np

import sensores


ancho, alto = 720,480

AZUL = (6,197,214)
GRAY = sensores.color_esc('slategray')
TURQOISE = sensores.color_esc('turqoise')
DMAGENTA = sensores.color_esc('darkmagenta')
INDIGO = sensores.color_esc('indigo')
DODGE = sensores.color_esc('dodgerblue')
BKG = (255,255,255)

FPS = 40
pygame.init()

vent = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption('Ondas')
clock = pygame.time.Clock()

sensors = [sensores.sonic(vent, (270,360), 'S1', c_off=GRAY),
           sensores.sonic(vent, (350,400), 'S2', c_off=GRAY),
           sensores.sonic(vent, (430,360), 'S3', c_off=GRAY)]

class onda(pygame.sprite.Sprite):
    def __init__(self, position, radio=0, velocidad=10, color=(0,0,0)):
        self.x = position[0]
        self.y = position[1]
        self.radius = radio
        self.color = color
        self.velocidad=velocidad

    def a_y_dibujar(self, window):
        self.radius+=self.velocidad
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, 1)

ondas = []

log = None
# log = []#Activar si deseo guardar registros de todas las actualizaciones de fps
utiles = []
pos = None
playground=False #permite el dibujo de varias ondas si esta en True
#Implementar modo de seguir al raton dibujando circulos de varios colores

time_left = 40
clean = time_left#FPS para eliminar valores de los sensores
contador=0#FPS para mostrar el circulo
running = True
while running:
   
        clock.tick(FPS)
        vent.fill(BKG)
        
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running=False
                pygame.quit(), sys.exit()

            elif e.type==pygame.MOUSEBUTTONDOWN:
                if playground is True:#se ejecuta desbloqueado
                    mpos = pygame.mouse.get_pos()
                    ondas.append(onda(mpos, color=DODGE))
                else:
                    if len(ondas)==0:
                        mpos = pygame.mouse.get_pos()
                        ondas.append(onda(mpos, color=TURQOISE))
                        print(f'Click {mpos}')

            elif e.type==pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running=False
                    pygame.quit(), sys.exit()
                elif e.key==pygame.K_KP0:
                    if len(ondas)>0:
                        if playground is True:
                            px = np.random.randint(ancho)
                            py = np.random.randint(alto)
                            ondas.append(onda((px,py), color=INDIGO))
                    else:
                        px = np.random.randint(ancho)
                        py = np.random.randint(alto)
                        ondas.append(onda((px,py), color=DODGE))
                elif e.key==pygame.K_KP1:
                    sensors[0].collide(True)
                elif e.key==pygame.K_KP2:
                    sensors[1].collide(True)
                elif e.key==pygame.K_KP3:
                    sensors[2].collide(True)
                elif e.key==pygame.K_KP_PERIOD:
                    position = (350, 300)
                    if playground is not True:
                        print(f'prueba equidistancia\t->\t{position}')
                    ondas.append(onda(position, color=DODGE))
                elif e.key==pygame.K_KP5:
                    esc_X = int(input('Indique la coordenada X:\t'))
                    esc_Y = int(input('Indique la coordenada Y:\t'))
                    ondas.append(onda((esc_X, esc_Y), color=DODGE))
                elif e.key==pygame.K_KP_ENTER:
                    ondas=[]
                    utiles=[]
                    playground = not playground
                    
        for i in ondas:
            i.a_y_dibujar(vent)
            if i.radius>800:
                del ondas[0]
                for j in sensors:
                    j.freeze(False)
                    # continue
            for detector in sensors:
                distance = np.sqrt((detector.x-i.x)**2+(detector.y-i.y)**2)
                if distance<=i.radius and i.radius*0.8<distance:
                    if detector.congelado==False:
                        detector.collide(True)
                        detector.freeze(True)
                        
        registro=[]
        for i in sensors:
            estado = i.state()
            apendice = estado.values()
            registro.append(list(apendice))
            if estado['status']==True:
                if playground is not True:
                    utiles.append(list(apendice))
            i.collide(False)
        if log is not None:
            log.append(registro)
        # print(registro)
           
        if len(utiles)>2:
            [print(f'\t{i}') for i in utiles]
            pos = sensores.triangular(utiles)
            utiles = []
            clean=time_left
        elif len(utiles)>0:
            clean-=1
            if clean<1:
                utiles=[]
                clean=time_left
            
        if pos is not None:
            if type(pos)==tuple:
                for point in sensors:
                    pygame.draw.line(vent, DMAGENTA, (point.x, point.y), (pos[0], pos[1]))
                pygame.draw.circle(vent, DMAGENTA, pos, 5)
                contador+=1
                if contador>time_left:                
                    contador=0
                    pos=None
            elif type(pos)==int:
                for point in sensors:
                    pygame.draw.circle(vent, INDIGO, (point.x, point.y), int(pos), 1)
                contador+=1
                if contador>time_left:                
                    contador=0
                    pos=None
            else:
                print(f'Error desconocido\t->\ttipo de variable: {type(pos)}')
            
        pygame.display.update()
    
