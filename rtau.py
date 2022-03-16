# function "rtau" in F-16 model used by function pdot.py


def rtau(dp):
    if dp <= 25.0:
        tau_r = 1.0  # reciprocal time constant
    elif dp >= 50.0:
        tau_r = 0.1
    else:
        tau_r = 1.9 - 0.036 * dp
    return tau_r
