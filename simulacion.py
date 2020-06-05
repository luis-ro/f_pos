
def main(screen, cuadros_seg, pos_sensores):
    import pygame, sys
    import numpy as np
    
    import sensores
    
    ancho, alto = screen
    max_size = ancho*1.1
    
    BLUE = (6,197,214)
    GRAY = sensores.color_esc('slategray')
    TURQOISE = sensores.color_esc('turqoise')
    DMAGENTA = sensores.color_esc('darkmagenta')
    INDIGO = sensores.color_esc('indigo')
    DODGE = sensores.color_esc('dodgerblue')
    CRIMSON = sensores.color_esc('crimson')
    BKG = (255,255,255)
    
    FPS = cuadros_seg
    pygame.init()
    
    vent = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption('waves')
    clock = pygame.time.Clock()
    
    sensors = []
    for i in pos_sensores:
        sensors.append(sensores.sonic(vent, pos_sensores[i], i, c_off=GRAY))
    num_sensors = len(sensors)
    
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
    
    utiles = []
    pos = None
    playground=False #if is True it's possible to draw any amount of waves at the same time
    test = None#Enable test mode aka key "t"
    #Implementar modo de seguir al raton dibujando circulos de varios colores
    
    running = True
    while running:
    
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
                            px,py = pygame.mouse.get_pos()
                            waves.append(wave((px,py), color=TURQOISE, speed=wave_speed))
                            print(f'Click ({px},{py})\tSpeed:{wave_speed}')
    
            elif e.type==pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running=False
                    pygame.quit(), sys.exit()
                elif e.key == pygame.K_t:
                    if test==True:
                        wave_speed+=5
                    test=True
                elif e.key==pygame.K_r:
                    test=False
                    wave_speed=10
                elif e.key==pygame.K_KP_ENTER or e.key==pygame.K_RETURN:
                    waves=[]
                    utiles=[]
                    playground = not playground
                    test = False
                elif e.key==pygame.K_UP:
                    wave_speed+=2
                elif e.key==pygame.K_DOWN:
                    wave_speed-=2
                    
                if test is not True:
                    if e.key==pygame.K_KP0 or e.key==pygame.K_0:
                        if len(waves)>0:
                            if playground is True:
                                px = np.random.randint(ancho)
                                py = np.random.randint(alto)
                                waves.append(wave((px,py), color=INDIGO, speed=wave_speed))
                        else:
                            px = np.random.randint(ancho)
                            py = np.random.randint(alto)
                            waves.append(wave((px,py), color=DODGE, speed=wave_speed))
                            print(f'Position: ({px},{py})\tSpeed:{wave_speed}')
                    elif e.key==pygame.K_KP_PERIOD or e.key==pygame.K_PERIOD:
                        px, py = 330,100
                        waves.append(wave((px, py), color=DODGE, speed=wave_speed))
                        if playground is not True:
                            print(f'Equidistant test\t->\t({px},{py})')
                    elif e.key==pygame.K_KP5 or e.key==pygame.K_5:
                        if len(waves)==0:
                            px = int(input('Specify X coordinate:\t'))
                            py = int(input('Specify Y coordinate:\t'))
                            print(f'({px}, {py})')
                            waves.append(wave((px, py), color=DODGE, speed=wave_speed))

        for i in waves:
            i.bigger(vent)
            if i.radius>max_size:
                del waves[0]
                for j in sensors:
                    j.freeze(False)
                    utiles = []
                    pos = None
            for detector in sensors:
                distance = np.sqrt((detector.x-i.x)**2+(detector.y-i.y)**2)
                if distance<=i.radius and i.radius*0.8<distance:
                    if detector.congelado==False:
                        detector.collide(True)
                        detector.freeze(True)
    
        if test == True:
            if len(waves)==0:
                px = np.random.randint(ancho)
                py = np.random.randint(alto)
                waves.append(wave((px, py), color=BLUE, speed=wave_speed))
                print(f'Position: ({px},{py})\tSpeed: {wave_speed}')
    
        registro=[]
        for i in sensors:
            estado = i.state()
            apendice = estado.values()
            registro.append(list(apendice))
            if estado['status']==True:
                if playground is not True:
                    utiles.append(list(apendice))
            i.collide(False)
           
        if len(utiles)==num_sensors:
            ordered=sorted(utiles, key=lambda k:k[0])#order by name
            pos = sensores.locate(ordered, cant_sensors=num_sensors, speed=waves[0].speed, real = (px,py))
            utiles = []
            
        if pos is not None:
            if type(pos)==tuple:
                for point in sensors:
                    pygame.draw.line(vent, CRIMSON, (point.x, point.y), (pos[0], pos[1]))
                pygame.draw.circle(vent, CRIMSON, pos, 5)
            else:
                print(f'Error desconocido\t->\tTipo de variable: {type(pos)}')
        pygame.display.update()

DIMENSIONS = (720,480)
CUADROS_FPS = 40

sens_dict = {'S1':(120,380),
             'S2':(330,450),
             'S3':(540,380)}

if __name__=='__main__':
    main(DIMENSIONS, CUADROS_FPS, sens_dict)
