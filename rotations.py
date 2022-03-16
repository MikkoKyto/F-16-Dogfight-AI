import numpy as np
from numpy import cos, sin
from math import atan2, asin



def FRD_to_NED(kulmat,vektori):
    p = kulmat[3] #roll
    q = kulmat[4] #pith
    r = kulmat[5] #yaw
    #p = atan2(sin(p)*cos(q),cos(p)*cos(q))
    #q = -asin(-sin(q))
    #r = atan2(cos(q)*sin(r),cos(q)*cos(r))
    RBI = np.asarray([[cos(q)*cos(r),cos(q)*sin(r),-sin(q)],
                      [(-cos(p)*sin(r)+sin(p)*sin(q)*cos(r)),cos(p)*cos(r)+sin(p)*sin(q)*sin(r),sin(p)*cos(q)],
                      [sin(p)*sin(r)+cos(p)*sin(q)*cos(r),(-sin(p)*cos(r)+cos(p)*sin(q)*sin(r)),cos(p)*cos(q)]])
    vektoriOut = np.dot(vektori,RBI)
    return vektoriOut

def NED_to_FRD(kulmat,vektori):
    p = kulmat[3]
    q = kulmat[4]
    r = kulmat[5]
    #p = atan2(sin(p)*cos(q),cos(p)*cos(q))
    #q = -asin(-sin(q))
    #r = atan2(cos(q)*sin(r),cos(q)*cos(r))
    RBI = np.asarray([[cos(q)*cos(r),(-cos(p)*sin(r)+sin(p)*sin(q)*cos(r)),sin(p)*sin(r)+cos(p)*sin(q)*cos(r)],
                      [cos(q)*sin(r),cos(p)*cos(r)+sin(p)*sin(q)*sin(r),(-sin(p)*cos(r)+cos(p)*sin(q)*sin(r))],
                      [-sin(q),sin(p)*cos(q),cos(-p)*cos(-q)]])
    vektoriOut = np.dot(vektori,RBI)
    return vektoriOut