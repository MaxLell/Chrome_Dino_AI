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

    # The creation of the this mating_pool leads to an exponential split in
    # fitness. The fittest dinos are exponentially represented. Therefore in the
    # long run, when only few Dinos make it far, only these will be able to
    # reproduce.

    mating_pool = []
    for dino in all_dinos:
        f = int(dino.fitness * len(all_dinos) * 10)
        for i in range(f):
            mating_pool.append(dino)

    # Sort mating pool by dino's fitness. Fittest dino becomes first element
    mating_pool = sorted(mating_pool, key = lambda dino: dino.fitness)[::-1]

    # natural selection: only the top 10% "survive" and are allowed to breed
    mating_pool = mating_pool[0:(len(mating_pool) // 10)]

    return mating_pool

# Step 3: Reproduction
def create_next_generation(population_size, dino_mating_pool):

    all_dinos = []
    active_dinos = []

    def crossover(father_DNA, mother_DNA): # Crossover
        # Due to the design of the create_mating_pool-function crossover becomes
        # more and more insignificant. At the end only clones of the same dinos
        # mate.

        crossover_DNA  = {}

        heritage_percentage = np.random.randint(11)*0.1

        for index in father_DNA.keys():
            # create a Deep copy of the father's DNA, so that the crossover_DNA
            # has the same shape as the former Generation
            crossover_DNA[index] = np.copy(father_DNA[index])

            orig_shape = father_DNA[index].shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    if np.random.random() < heritage_percentage:
                        crossover_DNA[index][i,j] = mother_DNA[index][i,j]

        return crossover_DNA

    def mutate(DNA):# Mutate

        def mutate_genome(S):
            orig_shape = S.shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    if np.random.random() < mutation_rate:
                        S[i,j] = np.random.randn() * mutation_magnitude

            return S.reshape(orig_shape)

        mutation_rate = 0.05
        # A higher mutation_rate leads to longer
        # stagnation at the beginning, but leads to faster game progressing in the long
        # run (fewer Dinos survive up until the higher tiers). A lower mutation_rate
        # leads to faster initial progress, but to slower longterm progress.
        # Any mutation_rate higher then 0.09 leads to longterm stagnation.

        mutation_magnitude = 0.1

        mutated_DNA = {}

        for i in DNA.keys(): # Mutate the DNA
            mutated_DNA[i] = mutate_genome(np.copy(DNA[i]))

        return mutated_DNA

    for i in range(population_size):

        # select random mating partners
        a = np.random.randint(0, len(dino_mating_pool))
        b = np.random.randint(0, len(dino_mating_pool))

        # Crossover and Mutation
        father_DNA = {}
        mother_DNA = {}

        for i in dino_mating_pool[0].brain.neural_wiring.keys():
            # The father's and the mother's DNA (neural wiring) are copied from the selected
            # Dinos from the dino_mating_pool.
            father_DNA[i] = np.copy(dino_mating_pool[a].brain.neural_wiring[i])
            mother_DNA[i] = np.copy(dino_mating_pool[b].brain.neural_wiring[i])

        crossover_DNA = crossover(father_DNA, mother_DNA)
        child_DNA     = mutate(crossover_DNA)

        # create a new child
        child = Dino()

        # inherit crossover-mutated DNA
        for i in child.brain.neural_wiring.keys():
            child.brain.neural_wiring[i] = child_DNA[i]

        all_dinos.append(child)
        active_dinos.append(child)

    return all_dinos, active_dinos
