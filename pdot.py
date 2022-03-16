# rate of change of power, i.e. pdot used in F-16 model
from rtau import rtau


def pdot(pow, cpow):
    # cpow = power level command, percent
    # pow = engine power level, percent

    if cpow >= 50.0:
        if pow >= 50.0:
            tpow = cpow
            t = 5.0
        else:
            tpow = 60.0
            t = rtau(tpow - pow)
    else:
        if pow >= 50.0:
            tpow = 40.0
            t = 5.0
        else:
            tpow = cpow
            t = rtau(tpow - pow)
    power_dot = t * (tpow - pow)
    return power_dot
