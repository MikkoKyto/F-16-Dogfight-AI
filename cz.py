#z-axis aerodynamic force coeff. in F-16 model
import numpy as np


def cz(alpha,beta,el):

    A = np.asarray([0.770, 0.241, -0.100, -0.416, -0.731, -1.053, -1.366, -1.646, -1.917, -2.120, -2.248, -2.229])
    A = np.transpose(A)
    row = 2

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

    s = A[int(k)+row] + abs(da) * (A[int(l)+row] - A[int(k)+row])
    cz_value = s * (1 - (beta / 57.3) ** 2) - 0.19 * (el / 25.0)

    return cz_value