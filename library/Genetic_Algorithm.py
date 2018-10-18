# All steps can be related to the algorithms proposed in the book
# "The Nature of Code - Chapter 9: Genetic Algorithms"

import numpy as np
from Dino import *

# Step 1
def create_new_population(population):
    active_dinos = []
    all_dinos = []

    for i in range(population):
        dino = Dino()
        active_dinos.append(dino) # important that both lists contain the same dinos
        all_dinos.append(dino)

    return all_dinos, active_dinos

# Step 2
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

# Step 3
def create_next_generation(population, dino_mating_pool):

    all_dinos = []
    active_dinos = []

    for i in range(population):
        a = np.random.randint(0, len(dino_mating_pool))
        b = np.random.randint(0, len(dino_mating_pool))

        # Crossover and Mutation in the dino.mate function
        child = dino_mating_pool[a].crossover(dino_mating_pool[b])

        all_dinos.append(child)
        active_dinos.append(child)

    return all_dinos, active_dinos
