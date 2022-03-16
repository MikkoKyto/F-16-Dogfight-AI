#pitching moment coefficients in F-16 model
import numpy as np


def cm(alpha, el):

    A = np.asarray([[.205, .168, .186, .196, .213, .251, .245, .238, .252, .231, .198, .192],
                    [.081, .077, .107, .110, .110, .141, .127, .119, .133, .108, .081, .093],
                    [-.046, -.020, -.009, -.005, -.006, .010, .006, -.001, .014, .000, -.013, .032],
                    [-.174, -.145, -.121, -.127, -.129, -.102, -.097, -.113, -.087, -.084, -.069, -.006],
                    [-.259, -.202, -.184, -.193, -.199, -.150, -.160, -.167, -.104, -.076, -.041, -.005]])
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
    cm_value = v + (w - v) * abs(de)
    return cm_value
