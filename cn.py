#yawing moment coefficients in F - 16model
import numpy as np


def cn(alpha, beta):
    A = np.asarray([[.0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0],
                    [.018, .019, .018, .019, .019, .018, .013, .007, .004, -.014, -.017, -.033],
                    [.038, .042, .042, .042, .043, .039, .030, .017, .004, -.035, -.047, -.057],
                    [.056, .057, .059, .058, .058, .053, .032, .012, .002, -.046, -.071, -.073],
                    [.064, .077, .076, .074, .073, .057, .029, .007, .012, -.034, -.065, -.041],
                    [.074, .086, .093, .089, .080, .062, .049, .022, .028, -.012, -.002, -.013],
                    [.079, .090, .106, .106, .096, .080, .068, .030, .064, .015, .011, -.001]])
    A = np.transpose(A)
    row = 2  # -1
    col = 0  # -1

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
    n = m + np.fix(np.sign(db) * 1.1)

    if n < 0:
        n = 0
    elif n > 6:
        n = 6

    t = A[int(k) + row, int(m) + col]
    u = A[int(k) + row, int(n) + col]
    v = t + abs(da) * (A[int(l) + row, int(m) + col] - t)
    w = u + abs(da) * (A[int(l) + row, int(n) + col] - u)
    dum = v + (w - v) * abs(db)
    cn_value = dum * np.sign(beta) * 1.0
    return cn_value
