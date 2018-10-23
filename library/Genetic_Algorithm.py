# All steps can be related to the algorithms proposed in the book
# "The Nature of Code - Chapter 9: Genetic Algorithms"

import numpy as np
from Dino import *

# Step 1: Create initial population
def create_new_population(population_size):
    active_dinos = []
    all_dinos = []

    for i in range(population_size):
        dino = Dino()
        active_dinos.append(dino) # important that both lists contain the same dinos
        all_dinos.append(dino)

    return all_dinos, active_dinos

# Step 2: Selection
def calculate_fitness(all_dinos):
    # get all dino scores and calculate for each dino
    # a normalized fitness score

    for dino in all_dinos:
        dino.score = dino.score**2

    sum = 0
    for dino in all_dinos:
        sum += dino.score

    for dino in all_dinos:
        dino.fitness = dino.score / sum

    return all_dinos

def create_mating_pool(all_dinos):
    # create a mating pool based on the dinos fitness
    # The higher the dino is in fitness, the more often it will be
    # represented in the mating pool. Therefore it will be selected
    # more often for reproduction (Step 3)

    mating_pool = []
    for dino in all_dinos:
        f = int(dino.fitness * len(all_dinos) * 10)
        for i in range(f):
            mating_pool.append(dino)

    # Sort mating pool by dino's fitness. Fittest dino becomes first element
    mating_pool = sorted(mating_pool, key = lambda dino: dino.fitness)[::-1]

    # natural selection: only the top 25% survive
    mating_pool = mating_pool[0:(len(mating_pool) // 4)]

    return mating_pool

# Step 3: Reproduction
def create_next_generation(population_size, dino_mating_pool):

    all_dinos = []
    active_dinos = []

    def crossover(dino_1, dino_2): # Crossover
        # split genome in half - one half from father, one half from mother
        # have incredible sexy time

        father_DNA = {}
        mother_DNA = {}
        child_DNA  = {}

        father_DNA['W1'] = np.copy(dino_1.brain.W1)
        father_DNA['b1'] = np.copy(dino_1.brain.b1)
        father_DNA['W2'] = np.copy(dino_1.brain.W2)
        father_DNA['b2'] = np.copy(dino_1.brain.b2)

        mother_DNA['W1'] = np.copy(dino_2.brain.W1)
        mother_DNA['b1'] = np.copy(dino_2.brain.b1)
        mother_DNA['W2'] = np.copy(dino_2.brain.W2)
        mother_DNA['b2'] = np.copy(dino_2.brain.b2)

        child_DNA['W1'] = np.copy(dino_1.brain.W1)
        child_DNA['b1'] = np.copy(dino_1.brain.b1)
        child_DNA['W2'] = np.copy(dino_1.brain.W2)
        child_DNA['b2'] = np.copy(dino_1.brain.b2)

        for index in father_DNA.keys():
            orig_shape = father_DNA[index].shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    if np.random.random() < 0.5:
                        child_DNA[index][i,j] = mother_DNA[index][i,j]

        return child_DNA

    def mutate(DNA):# Mutate

        mutation_rate = 0.05
        mutation_magnitude = 0.03

        # mutate genome
        def mutate_genome(S):
            orig_shape = S.shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    if np.random.random() < mutation_rate:
                        S[i,j] += np.random.randn() * mutation_magnitude

            return S.reshape(orig_shape)

        child = Dino()

        # create a small variation in child_brain #
        child.brain.W1 = mutate_genome(DNA['W1'])
        child.brain.b1 = mutate_genome(DNA['b1'])
        child.brain.W2 = mutate_genome(DNA['W2'])
        child.brain.b2 = mutate_genome(DNA['b2'])

        return child

    for i in range(population_size):
        a = np.random.randint(0, len(dino_mating_pool))
        b = np.random.randint(0, len(dino_mating_pool))

        # Crossover and Mutation in the dino.mate function
        child_DNA = crossover(dino_mating_pool[a], dino_mating_pool[b])
        child = mutate(child_DNA)

        all_dinos.append(child)
        active_dinos.append(child)

    return all_dinos, active_dinos
