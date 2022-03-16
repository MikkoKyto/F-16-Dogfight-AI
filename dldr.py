# rolling moment due to rudder in F-16 model
import numpy as np


def dldr(alpha, beta):
    A = np.asarray([[.005, .017, .014, .010, -.005, .009, .019, .005, .000, -.005, -.011, .008],
                    [.007, .016, .014, .014, .013, .009, .012, .005, .000, .004, .009, .007],
                    [.013, .013, .011, .012, .011, .009, .008, .005, .000, .005, .003, .005],
                    [.018, .015, .015, .014, .014, .014, .014, .015, .013, .011, .006, .001],
                    [.015, .014, .013, .013, .012, .011, .011, .010, .008, .008, .007, .003],
                    [.021, .011, .010, .011, .010, .009, .008, .010, .006, .005, .000, .001],
                    [.023, .010, .011, .011, .011, .010, .008, .010, .006, .014, .020, .000]])
    A = np.transpose(A)
    row = 2
    col = 3

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

    s = 0.1 * beta
    m = np.fix(s)
    if m <= -3:
        m = -2

    if m >= 3:
        m = 2

    db = s - m
    n = m + np.fix(np.sign(db) * 1.1)

    if n < -3:
        n = -3
    elif n > 3:
        n = 3

    t = A[int(k) + row, int(m) + col]
    u = A[int(k) + row, int(n) + col]
    v = t + abs(da) * (A[int(l) + row, int(m) + col] - t)
    w = u + abs(da) * (A[int(l) + row, int(n) + col] - u)
    dldr_value = v + (w - v) * abs(db)
    return dldr_value
