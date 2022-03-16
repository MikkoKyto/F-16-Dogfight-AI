# power command vs. thtl. relationship used in F-16 model


def tgear(thtl):
    if thtl <= 0.77:
        tgear_value = 64.94 * thtl
    else:
        tgear_value = 217.38 * thtl - 117.38
    return tgear_value
