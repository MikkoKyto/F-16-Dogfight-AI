from random import seed
from random import random
from math import tanh
import numpy as np



# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer1 = [{'weights': [random()*2.0-1.0 for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer1)
    hidden_layer2 = [{'weights': [random()*2.0-1.0 for i in range(n_hidden + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer2)
    hidden_layer3 = [{'weights': [random()*2.0-1.0 for i in range(n_hidden + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer3)
    output_layer = [{'weights': [random()*2.0-1.0 for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network




# Calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation



# Transfer neuron activation
def transfer(activation):
    return tanh(activation)  # tanh normalizes value -1.0 to 1.0


# Forward propagate input to a network output
def forward_propagate(network, x):
    inputs = x

    # Delete scores from network array
    # HOX!!! Needs to be modified if adding or deleting layers. HOX!!!
    if len(network) == 5:
        del network[4]

    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

#Genetic algorithm. Replaces bottom half of population with offsprings. Not in use atm.
def evolution_algorithm(population):
    offsprings = []
    half = int(len(population)/2)

    del population[-half:]
    net = 0

    for network in population:
        new_network = []
        lay = 0
        if len(network) == 5:
            del network[4]

        for layer in network:
            new_neuron = []
            neu = 0

            for neuron in layer:
                if net == 0:
                    parent1 = population[net][lay][neu]
                    parent2 = population[net+2][lay][neu]
                else:
                    parent1 = population[net-1][lay][neu]
                    parent2 = population[net][lay][neu]
                new_weights = crossbreed(parent1['weights'],parent2['weights'])
                new_neuron.append(new_weights)
                neu = neu + 1

            new_network.append(new_neuron)
            lay = lay +1

        offsprings.append(new_network)
        net = net+1

    population = population + offsprings
    return population

#Crosbreed and mutation
#sel values can be adjusted as prefered
def crossbreed(parent1, parent2):
    i = 0
    new_weights = []
    for weight in parent1:
        sel = random()
        if sel < 0.01: #Mutation rate
            new_weight = random()*2.0-1.0 #Random mutation
        elif sel > 0.52: #Propability of selecting weight from parent 2
            new_weight = parent2[i]
        else:
            new_weight = parent1[i]
        new_weights.append(new_weight)
        i = i + 1
    dic_new_weights = {'weights': new_weights}
    return dic_new_weights

# Genetic algorithm with roulette wheel selection and elitism
def ga_roulette(population):
    popsize = int(len(population))
    elitism = 10 #number of elites that will direcly transfer to next generation

    # Computes the totallity of the population fitness for roulette
    total = 0.0
    for network in population:
        if network[4]['score']<0.0:
            network[4]={'score': 0.0}
        total =total + network[4]['score']


    # Computes for each network the probability for roulette
    population_probabilities = []
    for network in population:
        network_fitness = network[4]['score']
        population_probabilities.append(network_fitness/total)
        del network[4]

    # Initialize offsprings
    offsprings=[]

    # Generate offsprings
    for i in range(int(popsize-elitism)):
        # Parent selection using roulette wheel
        p1_selection = np.random.choice(popsize, p=population_probabilities)
        parent_1 = population[p1_selection]
        p2_selection = np.random.choice(popsize, p=population_probabilities)
        parent_2 = population[p2_selection]

        new_network = []
        lay = 0

        #iterate trough layes in network
        for layer in parent_1:
            new_neuron = []
            neu = 0

            # Iterate trough neurons in netwok
            for neuron in layer:
                #select parent neurons
                parent1 = parent_1[lay][neu]
                parent2 = parent_2[lay][neu]
                #Crosbreed weights in neuron
                new_weights = crossbreed(parent1['weights'], parent2['weights'])
                new_neuron.append(new_weights)
                neu = neu + 1

            new_network.append(new_neuron)
            lay = lay + 1

        offsprings.append(new_network)

    #Append offspring to elites to create new generation
    population = population[:elitism] + offsprings
    return population







