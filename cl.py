#rolling moment coefficients in F-16 model
import numpy as np


def cl(alpha, beta):

    A = np.asarray([[.0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0],
                    [-.001, -.004, -.008, -.012, -.016, -.022, -.022, -.021, -.015, -.008, -.013, -.015],
                    [-.003, -.009, -.017, -.024, -.030, -.041, -.045, -.040, -.016, -.002, -.010, -.019],
                    [-.001, -.010, -.020, -.030, -.039, -.054, -.057, -.054, -.023, -.006, -.014, -.027],
                    [.000, -.010, -.022, -.034, -.047, -.060, -.069, -.067, -.033, -.036, -.035, -.035],
                    [.007, -.010, -.023, -.034, -.049, -.063, -.081, -.079, -.060, -.058, -.062, -.059],
                    [.009, -.011, -.023, -.037, -.050, -.068, -.089, -.088, -.091, -.076, -.077, -.076]])
    A = np.transpose(A)
    row = 2
    col = 0

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

    s = 0.2 * abs(beta)
    m = np.fix(s)
    if m == 0:
       m = 1

    if m >= 6:
       m = 5

    db = s - m
    n = m + np.fix(np.sign(db) * 1.1 )

    if n < 0:
        n = 0
    elif n > 6:
        n = 6

    t = A[int(k)+row, int(m)+col]
    u = A[int(k)+row, int(n)+col]
    v = t + abs(da) * (A[int(l)+row, int(m)+col] - t)
    w = u + abs(da) * (A[int(l)+row, int(n)+col] - u)
    dum = v + (w - v) * abs(db)
    cl_value = dum * np.sign(beta) * 1.0
    return cl_value
