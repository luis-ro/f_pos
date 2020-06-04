
from simulacion import DIMENSIONS as screen
from simulacion import sens_dict as positions
from numpy.random import randint as rn

import numpy as np
# =============================================================================
speed = None
num_valores = input('How many points do you want? [50k]\t\t')
if len(num_valores)==0:
    num_valores=50000
else:
    num_valores = int(num_valores)
    
change_speed = input('Constant speed? [(N)/Specify integer]\t')
if len(change_speed)!=0:
    speed=int(change_speed)
    change_speed=False
else:
    change_speed=True
    
guardar = input('Do you want to save? [(S)/N]\t\t')

for i in range(num_valores):
    if change_speed==True:
        speed = rn(10,25)
    log = f's={speed}\t'
    activation = []
    control = []
    continuar = True
    if num_valores==1:
        x,y = 585,299
    else:
        x = rn(screen[0])
        y = rn(screen[1])
    log+=f'({x};{y})\t'
    radio = 0
    for comparate in range(10*speed):
        radio+=1*speed
        cont = 0
        for sensor in positions.values():
            cont+=1
            distance = int(np.sqrt((x-sensor[0])**2+(y-sensor[1])**2))
            if distance>radio*0.8 and distance<=radio:
                if not (cont in control):
                    # print('\t\tOn\t',cont,':',comparate)
                    control.append(cont)
                    name = 'S'+str(cont)
                    activation.append([name, comparate])
                    if len(activation)==len(positions):
                        continuar = False
                        break
        if continuar == False:
            break

    preprocess=[activation[0]]
    for j in range(1,len(activation)):
        dt = activation[j][1]-activation[j-1][1]
        preprocess.append([activation[j][0], dt])
    preprocess[0][1]=0
    for k in preprocess:
        log+=f'{k[0]}:{k[1]}\t'
    log+='\n'
    
    if guardar.lower()!='n':
        try:
            f = open('test_points.txt', 'a')
            f.write(log)
        except:
            f.close()
            print('\n\nUn error ocurrio!\n')
            raise
    else:
        print(log)

