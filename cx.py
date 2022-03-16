#x-axis aerodynamic force coeff. in F-16 model
import numpy as np


def cx(alpha,el,amach):

    A = np.asarray([[-0.099, -0.081, -0.081, -0.063, -0.025, 0.044, 0.097, 0.113, 0.145, 0.167, 0.174, 0.166],
                    [-0.048, -0.038, -0.040, -0.021,  0.016, 0.083, 0.127, 0.137, 0.162, 0.177, 0.179, 0.167],
                    [-0.022, -0.020, -0.021, -0.004,  0.032, 0.094, 0.128, 0.130, 0.154, 0.161, 0.155, 0.138],
                    [-0.040, -0.038, -0.039, -0.025,  0.006, 0.062, 0.087, 0.085, 0.100, 0.110, 0.104, 0.091],
                    [-0.083, -0.073, -0.076, -0.072, -0.046, 0.012, 0.024, 0.025, 0.043, 0.053, 0.047, 0.040]])
    A = np.transpose(A)
    row = 2
    col = 2

    s = 0.2 * alpha
    k = np.fix(s)
    if k <= -2:
        k = -1

    if k >= 9:
        k = 8

    da = s - k
    l = k + np.fix(np.sign(da) * 1.1)

    if l < -2:
        l = -2
    elif l > 9:
        l = 9

    s = el / 12.0
    m = np.fix(s)
    if m <= -2:
       m = -1

    if m >= 2:
       m = 1

    de = s - m
    n = m + np.fix(np.sign(de) * 1.1)

    if n < -2:
        n = -2
    elif n > 2:
        n = 2

    t = A[int(k)+row, int(m)+col]
    u = A[int(k)+row, int(n)+col]
    v = t + abs(da) * (A[int(l)+row, int(m)+col] - t)
    w = u + abs(da) * (A[int(l)+row, int(n)+col] - u)
    cx_value = v + (w - v) * abs(de)

    #Drag coefficient bias. Simulates Mach effect on DC. Not acctual aerodynamic data!
    ###### Can be deleted if needed ######
    if amach > 0.86 and amach < 1.07:
        bias = 1.0 + abs((abs(1-amach)-0.14)*100/14)*2
        cx_value = cx_value*bias
    if amach > 1.07:
        cx_value = cx_value * 2

    return cx_value
