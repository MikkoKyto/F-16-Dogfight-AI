#sideforce coefficient in F-16 model


def cy(beta, ail, rdr):
    cy_value = -0.02 * beta -0.021 * (ail/20.0) + 0.086 * (rdr / 30.0)
    return cy_value