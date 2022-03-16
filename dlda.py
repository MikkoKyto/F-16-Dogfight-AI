# rolling moment due to ailerons in F-16 model
import numpy as np


def dlda(alpha, beta):
    A = np.asarray([[-.041, -.052, -.053, -.056, -.050, -.056, -.082, -.059, -.042, -.038, -.027, -.017],
                    [-.041, -.053, -.053, -.053, -.050, -.051, -.066, -.043, -.038, -.027, -.023, -.016],
                    [-.042, -.053, -.052, -.051, -.049, -.049, -.043, -.035, -.026, -.016, -.018, -.014],
                    [-.040, -.052, -.051, -.052, -.048, -.048, -.042, -.037, -.031, -.026, -.017, -.012],
                    [-.043, -.049, -.048, -.049, -.043, -.042, -.042, -.036, -.025, -.021, -.016, -.011],
                    [-.044, -.048, -.048, -.047, -.042, -.041, -.020, -.028, -.013, -.014, -.011, -.010],
                    [-.043, -.049, -.047, -.045, -.042, -.037, -.003, -.013, -.010, -.003, -.007, -.008]])
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

    t = A[int(k)+row, int(m)+col]
    u = A[int(k)+row, int(n)+col]
    v = t + abs(da) * (A[int(l)+row, int(m)+col] - t)
    w = u + abs(da) * (A[int(l)+row, int(n)+col] - u)
    dlda_value = v + (w - v) * abs(db)
    return dlda_value
