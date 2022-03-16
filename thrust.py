# engine thrust model in F-16 model
import numpy as np


def thrust(pow, alt, rmach):
    # A - idle
    # B - military
    # C - maximum

    A = np.asarray([[1060.0, 670.0, 880.0, 1140.0, 1500.0, 1860.0],
                    [635.0, 425.0, 690.0, 1010.0, 1330.0, 1700.0],
                    [60.0, 25.0, 345.0, 755.0, 1130.0, 1525.0],
                    [-1020.0, -710.0, -300.0, 350.0, 910.0, 1360.0],
                    [-2700.0, -1900.0, -1300.0, -247.0, 600.0, 1100.0],
                    [-3600.0, -1400.0, -595.0, -342.0, -200.0, 700.0]])
    A = np.transpose(A)

    B = np.asarray([[12680.0, 9150.0, 6200.0, 3950.0, 2450.0, 1400.0],
                    [12680.0, 9150.0, 6313.0, 4040.0, 2470.0, 1400.0],
                    [12610.0, 9312.0, 6610.0, 4290.0, 2600.0, 1560.0],
                    [12640.0, 9839.0, 7090.0, 4660.0, 2840.0, 1660.0],
                    [12390.0, 10176.0, 7750.0, 5320.0, 3250.0, 1930.0],
                    [11680.0, 9848.0, 8050.0, 6100.0, 3800.0, 2310.0]])
    B = np.transpose(B)

    C = np.asarray([[20000.0, 15000.0, 10800.0, 7000.0, 4000.0, 2500.0],
                    [21420.0, 15700.0, 11225.0, 7323.0, 4435.0, 2600.0],
                    [22700.0, 16860.0, 12250.0, 8154.0, 5000.0, 2835.0],
                    [24240.0, 18910.0, 13760.0, 9285.0, 5700.0, 3215.0],
                    [26070.0, 21075.0, 15975.0, 11115.0, 6860.0, 3950.0],
                    [28886.0, 23319.0, 18300.0, 13484.0, 8642.0, 5057.0]])
    C = np.transpose(C)

    row = 0
    col = 0

    h = 0.0001 * alt
    i = np.fix(h)
    if i >= 5:
        i = 4
    elif i <= 0:
        i = 0

    dh = h - i
    rm = 5.0 * rmach
    m = np.fix(rm)
    if m >= 5:
        m = 4
    elif m <= 0:
        m = 0

    dm = rm - m
    cdh = 1.0 - dh

    s = B[int(i) + row, int(m) + col] * cdh + B[int(i) + 1 + row, int(m) + col] * dh
    t = B[int(i) + row, int(m) + 1 + col] * cdh + B[int(i) + 1 + row, int(m) + 1 + col] * dh
    tmil = s + (t - s) * dm
    if pow < 50.0:
        s = A[int(i) + row, int(m) + col] * cdh + A[int(i) + 1 + row, int(m) + col] * dh
        t = A[int(i) + row, int(m) + 1 + col] * cdh + A[int(i) + 1 + row, int(m) + 1 + col] * dh
        tidl = s + (t - s) * dm
        thrust_value = tidl + (tmil - tidl) * pow * 0.02
    else:
        s = C[int(i) + row, int(m) + col] * cdh + C[int(i) + 1 + row, int(m) + col] * dh
        t = C[int(i) + row, int(m) + 1 + col] * cdh + C[int(i) + 1 + row, int(m) + 1 + col] * dh
        tmax = s + (t - s) * dm
        thrust_value = tmil + (tmax - tmil) * (pow - 50.0) * 0.02
    return thrust_value