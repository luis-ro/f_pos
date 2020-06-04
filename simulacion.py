
def main(screen, cuadros_seg, pos_sensores):
    import pygame, sys
    import numpy as np
    
    import sensores
    
    ancho, alto = screen
    
    BLUE = (6,197,214)
    GRAY = sensores.color_esc('slategray')
    TURQOISE = sensores.color_esc('turqoise')
    DMAGENTA = sensores.color_esc('darkmagenta')
    INDIGO = sensores.color_esc('indigo')
    DODGE = sensores.color_esc('dodgerblue')
    BKG = (255,255,255)
    
    FPS = cuadros_seg
    pygame.init()
    
    vent = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption('waves')
    clock = pygame.time.Clock()
    
    sensors = []
    for i in pos_sensores:
        sensors.append(sensores.sonic(vent, pos_sensores[i], i, c_off=GRAY))
    num_sensores = len(sensors)
    
    class wave(pygame.sprite.Sprite):
        def __init__(self, position, radio=0, speed=10, color=(0,0,0)):
            self.x = position[0]
            self.y = position[1]
            self.radius = radio
            self.color = color
            self.speed=speed
    
        def bigger(self, window):
            self.radius+=self.speed
            pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, 1)
    
    wave_speed = 10
    waves = []
    
    log = None
    # log = []#Activar si deseo guardar registros de todas las actualizaciones de fps
    utiles = []
    pos = None
    playground=False #if is True it's possible to draw any amount of waves at the same time
    test = None
    #Implementar modo de seguir al raton dibujando circulos de varios colores
    
    count=0#number of FPS to know when to turn off the circles
    running = True
    while running:
    
        time_left = 5+600/(wave_speed+10)#max time before resetting count in sensors
        clean = time_left#FPS remaining to delete sensors data
    
        clock.tick(FPS)
        vent.fill(BKG)
        
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running=False
                pygame.quit(), sys.exit()
    
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if test is not True:
                    if playground is True:
                        mpos = pygame.mouse.get_pos()
                        waves.append(wave(mpos, color=DODGE))
                    else:
                        if len(waves)==0:
                            mpos = pygame.mouse.get_pos()
                            waves.append(wave(mpos, color=TURQOISE, speed=wave_speed))
                            print(f'Click {mpos}')
    
            elif e.type==pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running=False
                    pygame.quit(), sys.exit()
                elif e.key == pygame.K_t:
                    if test is not False:
                        wave_speed+=5
                    test=True
                elif e.key==pygame.K_f:
                    test=False
                    wave_speed=10
                elif e.key==pygame.K_KP_ENTER:
                    waves=[]
                    utiles=[]
                    playground = not playground
                    test = False
                    
                if test is not True:
                    if e.key==pygame.K_KP0:
                        if len(waves)>0:
                            if playground is True:
                                px = np.random.randint(ancho)
                                py = np.random.randint(alto)
                                waves.append(wave((px,py), color=INDIGO, speed=wave_speed))
                        else:
                            px = np.random.randint(ancho)
                            py = np.random.randint(alto)
                            waves.append(wave((px,py), color=DODGE, speed=wave_speed))
                    elif e.key==pygame.K_KP1:
                        sensors[0].collide(True)
                    elif e.key==pygame.K_KP2:
                        sensors[1].collide(True)
                    elif e.key==pygame.K_KP3:
                        sensors[2].collide(True)
                    elif e.key==pygame.K_KP_PERIOD:
                        position = (330, 100)
                        waves.append(wave(position, color=DODGE, speed=wave_speed))
                        if playground is not True:
                            print(f'Equidistant test\t->\t{position}')
                    elif e.key==pygame.K_KP5:
                        if len(waves)==0:
                                px = np.random.randint(ancho)
                                py = np.random.randint(alto)
                                print(f'({px}, {py})')
                                waves.append(wave((px,py), color=INDIGO, speed=wave_speed))
                    elif e.key==pygame.K_KP8:
                        if len(waves)==0:
                            esc_X = int(input('Specify X coordinate:\t'))
                            esc_Y = int(input('Specify Y coordinate:\t'))
                            print(f'({esc_X}, {esc_Y})')
                            waves.append(wave((esc_X, esc_Y), color=DODGE, speed=wave_speed))


        for i in waves:
            i.bigger(vent)
            if i.radius>800:
                del waves[0]
                for j in sensors:
                    j.freeze(False)
            for detector in sensors:
                distance = np.sqrt((detector.x-i.x)**2+(detector.y-i.y)**2)
                if distance<=i.radius and i.radius*0.8<distance:
                    if detector.congelado==False:
                        detector.collide(True)
                        detector.freeze(True)
    
        if test == True:
            if len(waves)==0:
                waves.append(wave((np.random.randint(ancho), np.random.randint(alto)), color=BLUE, speed=wave_speed))
    
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
           
        if len(utiles)>num_sensores-1:
            [print(f'\t{i}') for i in utiles]
            pos = sensores.locate(utiles, wave_speed)
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
                count+=1
                if count>time_left:                
                    count=0
                    pos=None
            elif type(pos)==int:
                for point in sensors:
                    pygame.draw.circle(vent, INDIGO, (point.x, point.y), int(pos), 1)
                count+=1
                if count>time_left:                
                    count=0
                    pos=None
            else:
                print(f'Error desconocido\t->\ttipo de variable: {type(pos)}')
            
        pygame.display.update()

DIMENSIONS = (720,480)
CUADROS_FPS = 40

sens_dict = {'S1':(120,380), 'S2':(330,450), 'S3':(540,380)}

if __name__=='__main__':
    main(DIMENSIONS, CUADROS_FPS, sens_dict)
