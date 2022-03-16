import math
import numpy as np
# [6] = alt feet
# [8] = alpha rad
# [9] = beta rad
# [10] = Forward, [11] = Right, [12] = Down
def scoring (inputs):
    score = 0.0
    inputs[10] = inputs[10] * 6000.0
    inputs[11] = inputs[11] * 6000.0
    inputs[12] = inputs[12] * 6000.0
    inputs[23] = inputs[23] * 6000.0 #adversary F
    inputs[8] = inputs[8] * math.pi #alpha to rads
    inputs[7] = inputs[7] * 9.0



    aim = math.sqrt(inputs[11]**2 + inputs[12]**2) #aim error ft
    ata = math.atan(aim/abs(inputs[10])) #ATA rad
    dist = abs(math.sqrt(inputs[10]**2 + inputs[11]**2 + inputs[12]**2)) #Distance between AC ft


    if inputs[10]<0.0:
        ata = math.pi - ata

    #score per aim error
    score = ((math.pi - ata)/math.pi)**2

    #score per distance
    if inputs[10] > 0.0:
        if inputs[23] < 0.0:
            if dist < 6000.0:
                score = score + (1.0 - dist/6000.0)

    #aim error < 100ft

    if inputs[10] > 0.0:
        if aim < 500.0:
            score = 1.0
        if aim < 100.0:
            score = 10.0
        if aim < 15.0:
            score = 100.0

    #alt < 0ft
    if inputs[6] > 1.0:
        score = -1000.0

    #aoa limits
    if np.degrees(inputs[8]) > 55.0:
        score = -1.0
    if np.degrees(inputs[8]) < -55.0:
        score = -1.0

    #sideslip limits
    if np.degrees(inputs[9]) < -20.0:
        score = -1.0

    if np.degrees(inputs[9]) > 20.0:
        score = -1.0

    #Nz Limit
   
    if inputs[7] > 9.0:
        score = -1.0


    return score


