# yawing moment due to ailerons in F-16 model
import numpy as np


def dnda(alpha, beta):
    A = np.asarray([[.001, -.027, -.017, -.013, -.012, -.016, .001, .017, .011, .017, .008, .016],
                    [.002, -.014, -.016, -.016, -.014, -.019, -.021, .002, .012, .016, .015, .011],
                    [-.006, -.008, -.006, -.006, -.005, -.008, -.005, .007, .004, .007, .006, .006],
                    [-.011, -.011, -.010, -.009, -.008, -.006, .000, .004, .007, .010, .004, .010],
                    [-.015, -.015, -.014, -.012, -.011, -.008, -.002, .002, .006, .012, .011, .011],
                    [-.024, -.010, -.004, -.002, -.001, .003, .014, .006, -.001, .004, .004, .006],
                    [-.022, .002, -.003, -.005, -.003, -.001, -.009, -.009, -.001, .003, -.002, .001]])
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
    dnda_value = v + (w - v) * abs(db)
    return dnda_value
