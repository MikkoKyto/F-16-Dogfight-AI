# 6-DOF full nonlinear model for F-16 aircraft
# ---- State Variables --------
# x = [ vt    ( ft/sec )    - velocity
#       alpha ( rad )       - angle of attack
#       beta  ( rad )       - sideslip angle
#       phi   ( rad )       - Euler angle
#       theta ( rad )       - Euler angle
#       psi   ( rad )       - Euler angle
#       P     ( rad/sec )   - roll rate
#       Q     ( rad/sec )   - pitch rate
#       R     ( rad/sec )   - yaw rate
#       integral of north speed    ( ft )  - north displacement
#       integral of east speed     ( ft )  - east displacement
#       integral of vertical spped ( ft )  - altitude
#       pow  ( percent, 0 <= pow <= 100 )   - power ]
#
# ---- control Variables --------
# u = [ thtl ( 0 <= thtl <= 1.0 ) - throttle
#       el   ( deg )              - elevator
#       ail  ( deg )              - aileron
#       rdr  ( deg )              - rudder ]
#
# ---- parameters ---------
# xcg - center of gravity position as
#       fraction of mean aerodynamic chord
#
# ---- output Variables --------
# output = [ x_dot                - 1st order derivative of state x
#            an    ( ft/sec^2 )   - normal acceleration
#            alat  ( ft/sec^2 )   - lateral acceleration in y-axis
#            qbar  ( psf )        - dynamic pressure
#            amach                - mach number
#            q     ( rad/sec )    - pitch rate
#            alpha ( rad )        - angle of attack]

from numpy import cos, sin, pi
from math import asin, atan2
from adc import adc
from tgear import tgear
from pdot import pdot
from thrust import thrust
from cx import cx
from cy import cy
from cz import cz
from dlda import dlda
from dldr import dldr
from dnda import dnda
from dndr import dndr
from cl import cl
from cm import cm
from cn import cn
from damping import damping



def f16_dynam(x, control, xcg):
    # constant variables
    s = 300.0       # wing area (ft^2)
    b = 30.0        # wing span (ft^2)
    cbar = 11.32    # mean aerodynamic chord (ft)
    rm = 1.57e-3    # 1/mass
    xcgr = 0.35     # reference cg location (ft)
    he = 160.0      # engine angular momentum (slug-ft^2/s)

    # inertia constants
    c1 = -0.770
    c2 = 0.02755
    c3 = 1.055e-4
    c4 = 1.642e-6
    c5 = 0.9604
    c6 = 1.759e-2
    c7 = 1.792e-5
    c8 = -0.7336
    c9 = 1.587e-5

    rtod = 180 /pi #radians to degrees
    g = 32.174          #ft/s^2

    # assign state variables
    vt = x[0]
    alpha = x[1] * rtod # x(2) in radians, alpha in degrees.
    beta = x[2] * rtod # x(3) in radians, beta in degrees.
    phi = x[3]
    theta = x[4]
    psi = x[5]
    p = x[6]
    q = x[7]
    r = x[8]
    alt = x[11]
    pow = x[12] #power

    # initialize state dot list
    x_dot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Assign control variables
    thtl = control[0]
    el = control[1]
    ail = control[2]
    rdr = control[3]

    # Air Data computer and engine model
    atmos = adc(vt, alt)
    tfac = atmos[0]
    t = atmos[1]
    rho = atmos[2]
    amach = atmos[3]
    qbar = atmos[4]
    ps = atmos[5]

    cpow = tgear(thtl)
    x_dot[12] = pdot(pow, cpow) # x_dot[12] = power derivative
    t = thrust(pow, alt, amach)

    # Look-up tables and component buildup
    cxt = cx(alpha, el, amach)
    cyt = cy(beta, ail, rdr)
    czt = cz(alpha, beta, el)
    dail = ail / 20.0
    drdr = rdr / 30.0
    dlda_value = dlda(alpha, beta)
    dldr_value = dldr(alpha, beta)
    clt = cl(alpha, beta) + dlda_value * dail + dldr_value * drdr
    cmt = cm(alpha, el)
    dnda_value = dnda(alpha, beta)
    dndr_value = dndr(alpha, beta)
    cnt = cn(alpha, beta) + dnda_value * dail + dndr_value * drdr

    # Add damping derivatives
    tvt = 0.5 / vt
    b2v = b * tvt
    cq = cbar * q * tvt
    d = damping(alpha)
    cxt = cxt + cq * d[0]
    cyt = cyt + b2v * (d[1] * r + d[2] * p)
    czt = czt + cq * d[3]
    clt = clt + b2v * (d[4] * r + d[5] * p)
    cmt = cmt + cq * d[6] + czt * (xcgr - xcg)
    cnt = cnt + b2v * (d[7] * r + d[8] * p) - cyt * (xcgr - xcg) * cbar / b

    # Get ready for state equations
    cbta = cos(x[2])
    u = vt * cos(x[1]) * cbta
    v = vt * sin(x[2])
    w = vt * sin(x[1]) * cbta
    sth = sin(theta)
    cth = cos(theta)
    sph = sin(phi)
    cph = cos(phi)
    spsi = sin(psi)
    cpsi = cos(psi)
    qs = qbar * s
    qsb = qs * b
    rmqs = rm * qs
    gcth = g * cth
    qsph = q * sph
    ay = rmqs * cyt
    az = rmqs * czt

    #correct alpha
    alpha = atan2(w,u)
    beta = asin(v/x[0])

    # Force equations
    udot = r * v - q * w - g * sth + rm * (qs * cxt + t)
    vdot = p * w - r * u + gcth * sph + ay
    wdot = q * u - p * v + gcth * cph + az
    dum = (u * u + w * w)
    x_dot[0] = (u * udot + v * vdot + w * wdot) / vt
    x_dot[1] = (u * wdot - w * udot) / dum
    x_dot[2] = (vt * vdot - v * x_dot[0]) * cbta / dum


    # Kinematics
    x_dot[3] = p + (sth / cth) * (qsph + r * cph)
    x_dot[4] = q * cph - r * sph
    x_dot[5] = (qsph + r * cph) / cth


    # Moments
    x_dot[6] = (c2 * p + c1 * r + c4 * he) * q + qsb * (c3 * clt + c4 * cnt)
    x_dot[7] = (c5 * p - c7 * he) * r + c6 * (r ** 2 - p ** 2) + qs * cbar * c7 * cmt
    x_dot[8] = (c8 * p - c2 * r + c9 * he) * q + qsb * (c4 * clt + c9 * cnt)

    # Navigation
    t1 = sph * cpsi
    t2 = cph * sth
    t3 = sph * spsi
    s1 = cth * cpsi
    s2 = cth * spsi
    s3 = t1 * sth - cph * spsi
    s4 = t3 * sth + cph * cpsi
    s5 = sph * cth
    s6 = t2 * cpsi + t3
    s7 = t2 * spsi - t1
    s8 = cph * cth

    x_dot[9] = u * s1 + v * s3 + w * s6    # north speed
    x_dot[10] = u * s2 + v * s4 + w * s7   # east speed
    x_dot[11] = u * sth - v * s5 - w * s8  # vertical speed

    # output
    an = (-1) * az / g
    alat = ay / g


    return[x_dot, an, alat, qbar, amach, q, alpha, beta]
