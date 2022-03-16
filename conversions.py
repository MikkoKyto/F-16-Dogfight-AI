import numpy as np
from numpy import sin, cos, pi, sqrt
from adc import adc
from rotations import NED_to_FRD
import math


def normalize_euler_angles(x):
    x[3] = math.atan2(sin(x[3]) * cos(x[4]), cos(x[3]) * cos(x[4]))
    x[4] = -math.asin(-sin(x[4]))
    x[5] = math.atan2(cos(x[4]) * sin(x[5]), cos(x[4]) * cos(x[5]))

    return x


def restrict_alpha_and_beta(x, derivatives):
    x[1] = derivatives[6]
    if x[1] > pi:
        x[1] = -pi + (x[1] - pi)
    if x[1] < -pi:
        x[1] = pi + (x[1] + pi)
    if x[1] > pi:
        x[1] = pi
    if x[1] < -pi:
        x[1] = -pi

    x[2] = derivatives[7]
    if x[2] > pi/2:
        x[2] = pi/2
    if x[2] < -pi/2:
        x[2] = -pi/2

    return x

def normalize_input_data(os_x, ad_x, os_der, ad_der):
# x = [ vt    ( ft/sec )    x[0] - velocity
#       alpha ( rad )       x[1] - angle of attack
#       beta  ( rad )       x[2] - sideslip angle
#       phi   ( rad )       x[3] - Euler angle
#       theta ( rad )       x[4] - Euler angle
#       psi   ( rad )       x[5] - Euler angle
#       P     ( rad/sec )   x[6] - roll rate
#       Q     ( rad/sec )   x[7] - pitch rate
#       R     ( rad/sec )   x[8] - yaw rate
#       integral of north speed    ( ft )  x[9] - north displacement
#       integral of east speed     ( ft )  x[10]- east displacement
#       integral of vertical speed ( ft )  x[11]- altitude
#       pow  ( percent, 0 <= pow <= 100 )  x[12]- power ]

# der[x_dot, an, alat, qbar, amach, q, alpha, beta]
# der[0    , 1 , 2   , 3   , 4    , 5, 6    , 7   ]

    #initialize array
    net_input = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

    # eas
    atmos = adc(os_x[0], os_x[11])
    net_input[0] = os_x[0] * 0.592484 * sqrt(atmos[2] / 2.37764e-3) #Eas kts

    # u, v and w
    vt = os_x[0]
    cbta = cos(os_x[2])

    net_input[1] = vt * cos(os_x[1]) * cbta #u ft/s
    net_input[2] = vt * sin(os_x[2])        #v ft/s
    net_input[3] = vt * sin(os_x[1]) * cbta #w ft/s

    # roll and pitch
    net_input[4] = os_x[3] #roll rad
    net_input[5] = os_x[4] #pitch rad

    #alt
    net_input[6] = os_x[11] #alt ft

    #nz, alpha, beta
    net_input[7] = os_der[1] #nz G
    net_input[8] = os_x[1]  #alpha rad
    net_input[9] = os_x[2]  #beta rad

    #F, R and D displacement
    ned_os_to_ad_displ = np.asarray([ad_x[9] - os_x[9], ad_x[10] - os_x[10], -ad_x[11] + os_x[11]])

    frd_os_to_ad_displ =  NED_to_FRD(os_x, ned_os_to_ad_displ)
    net_input[10] = frd_os_to_ad_displ[0] #F ft
    net_input[11] = frd_os_to_ad_displ[1] #R ft
    net_input[12] = frd_os_to_ad_displ[2] #D ft


    #net_input[10] = ned_os_to_ad_displ[0]  # F ft
    #net_input[11] = ned_os_to_ad_displ[1]  # R ft
    #net_input[12] = ned_os_to_ad_displ[2]  # D ft

    ################### Adversary ###################

    #eas
    atmos = adc(ad_x[0], ad_x[11])
    net_input[13] = ad_x[0] * 0.592484 * sqrt(atmos[2] / 2.37764e-3)  # Eas kts


    # u, v and w
    vt = ad_x[0]
    cbta = cos(ad_x[2])

    net_input[14] = vt * cos(ad_x[1]) * cbta  # u ft/s
    net_input[15] = vt * sin(ad_x[2])  # v ft/s
    net_input[16] = vt * sin(ad_x[1]) * cbta  # w ft/s


    # roll and pitch
    net_input[17] = ad_x[3]  # roll rad
    net_input[18] = ad_x[4]  # pitch rad

    # alt
    net_input[19] = ad_x[11]  # alt ft

    # na, alpha, beta
    net_input[20] = ad_der[1]  # na G
    net_input[21] = ad_x[1]  # alpha rad
    net_input[22] = ad_x[2]  # beta rad


    # F, R and D displacement
    ned_ad_to_os_displ = np.asarray([os_x[9] - ad_x[9], os_x[10] - ad_x[10], -os_x[11] + ad_x[11]])
    frd_ad_to_os_displ = NED_to_FRD(ad_x, ned_ad_to_os_displ)
    net_input[23] = frd_ad_to_os_displ[0]  # F ft
    net_input[24] = frd_ad_to_os_displ[1]  # R ft
    net_input[25] = frd_ad_to_os_displ[2]  # D ft


    #net_input[23] = ned_ad_to_os_displ[0]  # F ft
    #net_input[24] = ned_ad_to_os_displ[1]  # R ft
    #net_input[25] = ned_ad_to_os_displ[2]  # D ft

    # net_inputs[]
    # [0] = eas ( kts )     - Equivalent airspeed
    # [1] = u   ( ft/s )    - Axial velocity
    # [2] = v   ( ft/s )    - Lateral velocity
    # [3] = w   ( ft/s )    - Normal velocity
    # [4] = phi ( rad )     - euler angle (roll)
    # [5] = theta ( rad )   - euler angle (pitch)
    # [6] = alt ( ft )      - altitude
    # [7] = na  ( g )       - normal acceleration elikkäs g-voima
    # [8] = alpha ( rad )   - angle of attack
    # [9] = beta ( rad )    - angle of sideslip
    # [10] = forward ( ft ) - forward displacement of adversary in FRD
    # [11] = right  ( ft )  - right side displacement of adversary in FRD
    # [12] = down ( ft )    - down displacement of adversary in FRD
    ######### adversary ##########
    # [13] = eas
    # [14] = u
    # [15] = v
    # [16] = w
    # [17] = phi
    # [18] = theta
    # [19] = alt
    # [20] = na
    # [21] = alpha
    # [22] = beta
    # [23] = forward
    # [24] = right
    # [25] = down

    #normalize net_inputs
    net_input[0] = net_input[0] / 666.0 # 666.0 kts ~ 1.0M at sea level
    net_input[1] = net_input[1] / 1124.0 # 1124.0 ft/s ~ 1.0M at sea level
    net_input[2] = net_input[2] / 1124.0
    net_input[3] = net_input[3] / 1124.0
    net_input[4] = net_input[4] / pi
    net_input[5] = net_input[5] / (pi/2.0)
    net_input[6] = 1 - (net_input[6] / 20000.0)
    net_input[7] = net_input[7] / 9.0
    net_input[8] = net_input[8] / pi
    net_input[9] = net_input[9] / (pi/2.0)
    net_input[10] = net_input[10] / 6000.0
    net_input[11] = net_input[11] / 6000.0
    net_input[12] = net_input[12] / 6000.0

    #### adversary ####
    net_input[13] = net_input[13] / 666.0  # 666.0 kts ~ 1.0M at sea level
    net_input[14] = net_input[14] / 1124.0  # 1124.0 ft/s ~ 1.0M at sea level
    net_input[15] = net_input[15] / 1124.0
    net_input[16] = net_input[16] / 1124.0
    net_input[17] = net_input[17] / pi
    net_input[18] = net_input[18] / (pi / 2.0)
    net_input[19] = 1 - (net_input[19] / 20000.0)
    net_input[20] = net_input[20] / 9.0
    net_input[21] = net_input[21] / pi
    net_input[22] = net_input[22] / (pi / 2.0)
    net_input[23] = net_input[23] / 6000.0
    net_input[24] = net_input[24] / 6000.0
    net_input[25] = net_input[25] / 6000.0

    return net_input





