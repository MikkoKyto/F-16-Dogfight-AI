from multiprocessing import Pool
import numpy as np
from f_16 import f16_dynam
from neuralnet import initialize_network, forward_propagate, evolution_algorithm, ga_roulette
from control import neural_control
from conversions import normalize_euler_angles, restrict_alpha_and_beta, normalize_input_data
from scoring import scoring
from functools import partial



def initialize_population(num):
    return initialize_network(26, 21, 4)  # (n_input, widenes, n_output)

def iterate_generation(i, population):
    print('ajo: ', i)


    # initialize departure check
    blue_dep = False
    red_dep = False

    # select networks
    b_network = population[i * 2 - 1]
    r_network = population[i * 2]

    # initialize state vector
    b_x = np.asarray(
        [800.0, 0.0, 0.0, np.radians(00.0), np.radians(0.0), np.radians(180.0), 0.0, 0.0, 0.0, 1000.0, 1000.0,
         10000.0, 0.0])
    r_x = np.asarray(
        [800.0, 0.0, 0.0, np.radians(00.0), np.radians(0.0), np.radians(0.0), 0.0, 0.0, 0.0, 0.0, 0.0, 10000.0,
         0.0])

    # x = [ vt    ( ft/sec )    x[0] - velocity
    #       alpha ( rad )       x[1] - angle of attack
    #       beta  ( rad )       x[2] - sideslip angle
    #       phi   ( rad )       x[3] - Euler angle
    #       theta ( rad )       x[4] - Euler angle
    #       psi   ( rad )       x[5] - Euler angle
    #       P     ( rad/sec )   x[6] - roll rate
    #       Q     ( rad/sec )   x[7] - pitch rate
    #       R     ( rad/sec )   x[8] - yaw rate
    #       integral of north speed    ( ft )  x[9] - north displacement
    #       integral of east speed     ( ft )  x[10]- east displacement
    #       integral of vertical speed ( ft )  x[11]- altitude
    #       pow  ( percent, 0 <= pow <= 100 )  x[12]- power ]

    # initialize Controls
    b_control = [1.0, 0.0, 0.0, 0.0]
    r_control = [1.0, 0.0, 0.0, 0.0]

    # control = [ thtl ( 0 <= thtl <= 1.0 ) - throttle
    #       el   ( deg )              - elevator
    #       ail  ( deg )              - aileron
    #       rdr  ( deg )              - rudder ]

    # initialize parameters
    xcg = 0.2
    # xcg - center of gravity position as fraction of mean aerodynamic chord
    # 0.2 ~ 0.5, reference xcg = 0.35

    # Define Time Variables
    timestep = 0.01

    # initialize scoring
    b_score = 0
    r_score = 0

    viewer = False
    hud_viewer = False
    manual_controls = False
    auto_controls = True

    for idx in range(24000):

        try:

            # Blue departure check starts
            blue_dep = True
            # Runge kutta four for blue
            k1 = timestep * np.asarray(f16_dynam(b_x, b_control, xcg)[0])
            k2 = timestep * np.asarray(f16_dynam(b_x + k1 / 2, b_control, xcg)[0])
            k3 = timestep * np.asarray(f16_dynam(b_x + k2 / 2, b_control, xcg)[0])
            k4 = timestep * np.asarray(f16_dynam(b_x + k3, b_control, xcg)[0])
            b_x_dot = (1 / 6 * (k1 + 2.0 * k2 + 2.0 * k3 + k4))
            b_x += b_x_dot

            # Make blue derivatives vector
            # [x_dot, an, alat, qbar, amach, q, alpha, beta]
            # [0    , 1 , 2   , 3   , 4    , 5, 6    , 7   ]
            b_derivatives = f16_dynam(b_x, b_control, xcg)

            # Check for blue ground kill
            if b_x[11] < 0.0:
                break
            # Blue Departure check ends
            blue_dep = False

            # Red departure check starts
            red_dep = True
            # Runge kutta four for red
            k1 = timestep * np.asarray(f16_dynam(r_x, r_control, xcg)[0])
            k2 = timestep * np.asarray(f16_dynam(r_x + k1 / 2, r_control, xcg)[0])
            k3 = timestep * np.asarray(f16_dynam(r_x + k2 / 2, r_control, xcg)[0])
            k4 = timestep * np.asarray(f16_dynam(r_x + k3, r_control, xcg)[0])
            r_x_dot = (1 / 6 * (k1 + 2.0 * k2 + 2.0 * k3 + k4))
            r_x += r_x_dot

            #Make red derivatives vector
            r_derivatives = f16_dynam(r_x, r_control, xcg)

            #Check for red ground kill
            if r_x[11] < 0.0:
                break
            red_dep = False

            # normalize eurel angles
            b_x = normalize_euler_angles(b_x)
            r_x = normalize_euler_angles(r_x)

            # restrict alpha and beta
            b_x = restrict_alpha_and_beta(b_x, b_derivatives)
            r_x = restrict_alpha_and_beta(r_x, r_derivatives)

            # ANN control for AC
            if auto_controls == True:
                # form imputs for neural net
                b_input = normalize_input_data(b_x, r_x, b_derivatives, r_derivatives)
                r_input = normalize_input_data(r_x, b_x, r_derivatives, b_derivatives)

                # forward propagate
                b_output = forward_propagate(b_network, b_input)
                r_output = forward_propagate(r_network, r_input)

                # new control commads
                b_control = neural_control(b_output)
                r_control = neural_control(r_output)

                # scoring

                b_score = b_score + scoring(b_input) * timestep
                r_score = r_score + scoring(r_input) * timestep

        # Departure handler
        except:

            if blue_dep == True:
                print("Blue departure")

            if red_dep == True:
                print("Red departure")

            break

    # Appending scores to networks
    blue_score = {'score': b_score}

    if len(b_network) == 4:
        population[i * 2 - 1].append(blue_score)
    else:
        del population[i * 2 - 1][-1:]
        population[i * 2 - 1].append(blue_score)

    red_score = {'score': r_score}

    if len(r_network) == 4:
        population[i * 2].append(red_score)
    else:
        del population[i * 2][-1:]
        population[i * 2].append(red_score)

    #Returns the two networks with scores appended
    two_networks = [population[i*2],population[i*2-1]]
    return two_networks

if __name__ == '__main__':

    # initialize population networks
    popsize = 80
    epocs = 100000
    half = int(popsize / 2)  # should be half of popsize


    p = Pool()
    population = p.map(initialize_population, [i for i in range(popsize)])
    p.close()


    # create save files
    savA_file = open("savA.txt", "w")
    savA_file.write("")
    savA_file.close()

    savB_file = open("savB.txt", "w")
    savB_file.write("")
    savB_file.close()

    savBN_file = open("savBN.txt", 'w')
    savBN_file.write("")
    savBN_file.close()

    #Visual options
    viewer = False
    hud_viewer = False
    #Control options
    manual_controls = False
    auto_controls = True



    for j in range(epocs):
        print('Epoc: ',j)
        p = Pool()
        population = p.map(partial(iterate_generation,population = population), [i for i in range(half)])
        p.close()

        new_population = []
        for k in range(half):
            for l in range(2):
                new_population.append(population[k][l])
        population = new_population

        # sort population by fitness
        if auto_controls == True:
            population.sort(key=lambda x: x[4]['score'], reverse=True)
            print(population[0])

            # save average score
            total = 0.0
            for network in population:
                total = total + network[4]['score']
            average = total / float(popsize)

            savA_file = open("savA.txt", 'a')
            ave = str(average) + "\n"
            savA_file.write(ave)
            savA_file.close()

            # save best score
            savB_file = open("savB.txt", 'a')
            best = str(population[0][4]['score']) + "\n"
            savB_file.write(best)
            savB_file.close()

            # save population
            savP_file = open("savP.txt", 'w')
            pop = str(population)
            savP_file.write(pop)
            savP_file.close()

            # save best
            savBN_file = open("savBN.txt", 'a')
            BN = str(population[0]) + "\n"
            savBN_file.write(BN)
            savBN_file.close()

            # Evolution
            population = ga_roulette(population)
            #population = evolution_algorithm(population)
