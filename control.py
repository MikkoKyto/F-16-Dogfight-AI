
def neural_control (output):

    lat_stick = (output[0] - output[1]) * 21.5
    pull = (output[2] - output[3]) * 25

    control = [1.0, pull, lat_stick, 0.0]

    return control