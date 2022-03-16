#various damping coefficients in F-16 model
import numpy as np

def damping(alpha):

        # d[0] = CXq
        # d[1] = CYr
        # d[2] = CYp
        # d[3] = CZq
        # d[4] = Clr
        # d[5] = Clp
        # d[6] = Cmq
        # d[7] = Cnr
        # d[8] = Cnp

    A = np.asarray([[-0.267, -0.110, 0.308, 1.34, 2.08, 2.91, 2.76, 2.05, 1.50, 1.49, 1.83, 1.21],
                    [0.882, 0.852, 0.876, 0.958, 0.962, 0.974, 0.819, 0.483, 0.590, 1.21, -0.493, -1.04],
                    [-0.108, -0.108, -0.188, 0.110, 0.258, 0.226, 0.344, 0.362, 0.611, 0.529, 0.298, -0.227],
                    [-8.80, -25.8, -28.9, -31.4, -31.2, -30.7, -27.7, -28.2, -29.0, -29.8, -38.3, -35.3],
                    [-0.126, -0.026, 0.063, 0.113, 0.208, 0.230, 0.319, 0.437, 0.680, 0.100, 0.447, -0.330],
                    [-0.360, -0.359, -0.443, -0.420, -0.383, -0.375, -0.329, -0.294, -0.230, -0.210, -0.120, -0.100],
                    [-7.21, -5.40, -5.23, -5.26, -6.11, -6.64, -5.69, -6.00, -6.20, -6.40, -6.60, -6.00],
                    [-0.380, -0.363, -0.378, -0.386, -0.370, -0.453, -0.550, -0.582, -0.595, -0.637, -1.02, -0.840],
                    [0.061, 0.052, 0.052, -0.012, -0.013, -0.024, 0.050, 0.150, 0.130, 0.158, 0.240, 0.150]])
    A = np.transpose(A)
    row = 2

    s = 0.2 * alpha
    k = np.fix(s)
    if k <= -2:
        k = -1
    elif k >= 9:
        k = 8

    da = s - k
    l = k + np.fix(np.sign(da) * 1.1)

    if l < -2:
        l = -2
    elif l > 9:
        l = 9

    d = []
    for i in range(9):
        d += [A[int(k) + row, i] + abs(da) * (A[int(l) + row, i] - A[int(k) + row, i])]
    np.asarray(d)

    d = np.transpose(d)  # transfer d into a column vector
    return d

