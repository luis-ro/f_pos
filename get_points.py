
from simulacion import DIMENSIONS as screen
from simulacion import sens_dict as positions
from numpy.random import randint as rn

import numpy as np
import csv
# =============================================================================
num_defecto = 2
file_name = 'test_points.csv'
# =============================================================================
speed = None
num_valores = input(f'How many points do you want? [{num_defecto/1000}k]\t\t')
if len(num_valores)==0:
    num_valores=num_defecto
else:
    num_valores = int(num_valores)

change_speed = input('Constant speed? [(N)/Specify integer]\t')
# change_speed='10'
if len(change_speed)!=0:
    speed=int(change_speed)
    change_speed=False
else:
    change_speed=True
    
first_row = ['W_speed','S1','S2','S3','waveX','waveY']
guardar = input('Do you want to save? [(S)/N]\t\t')
# guardar='n'
if guardar.lower()!='n':
    print('\t\tGuardando...')
    import os.path
    if os.path.exists(file_name)==False:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(first_row)
else:
    print(first_row)
    
for i in range(num_valores):
    if change_speed==True:
        speed = rn(10,25)
    activation = []
    control = []
    continuar = True
    if num_valores==1:
        x,y = 450,250
    else:
        x = rn(screen[0]*2/3, screen[0])
        y = rn(screen[1]/2, screen[1])
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
    smallest = min([i[1] for i in preprocess])
    for j in range(1,len(activation)):
        dt = activation[j][1]-smallest
        preprocess.append([activation[j][0], dt])
    preprocess[0][1]=0
    ordered = sorted(preprocess, key=lambda k:k[0])
    log = [speed]
    for k in ordered:
        log.append(k[1])
    log.append(x)
    log.append(y)
    
    if guardar.lower()!='n':
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(log)
    else:
        print(log)
print('\nListo!')
