import pygame as pg
from Brain import Dino_Brain
import numpy as np
import os

class Dino():

    def __init__(self):

        self.path        = os.getcwd() + '/' + 'Sprites' + '/'

        # Image Section
        self.img_run     = [pg.image.load(self.path + 'dino_run_0.png'),
                            pg.image.load(self.path + 'dino_run_1.png')]

        self.img_duck    = [pg.image.load(self.path + 'dino_duck_0.png'),
                            pg.image.load(self.path + 'dino_duck_1.png')]
        self.frame_run    = 0
        self.frame_duck   = 0

        # Property Section
        self.x           = 50
        self.y           = 237
        self.width       = 59
        self.height      = 63

        self.score = 0
        self.fitness = 0

        # Init Dino Brain
        self.brain = Dino_Brain()
        self.mutation_rate = 0.05

        self.jump_count = 10

        # Dino states
        self.is_running = True
        self.is_ducking = False
        self.is_jumping = False

    def sense_environment(self, obstacles):

        # inputs for NN
        observation_dict = {}
        if len(obstacles) == 0:
            # if no obstacles
            observation_dict['distance_dino_obstcl_x'] = 1
            observation_dict['obstcl_y'] = 1

        else:
            # Min-Max scaled features
            observation_dict['distance_dino_obstcl_x'] = (-1*self.x + obstacles[0].x) / 870
            observation_dict['obstcl_y'] = (obstacles[0].y) / 400

        observation_dict['dino_y'] = self.y / 400
        observation_dict['dino_y_vel'] = self.jump_count / 30
        observation_dict['bias'] = np.random.randn() * 0.1

        # place values in numpy array
        observation = np.array([observation_dict['distance_dino_obstcl_x'],
                                observation_dict['obstcl_y'],
                                observation_dict['dino_y'],
                                observation_dict['dino_y_vel'],
                                observation_dict['bias']])

        return observation

    def crossover(self, sexy_dino_girl): # Crossover
        # split genome in half - one half from father, one half from mother
        # have incredible sexy time

        # if you do not generate a deep copy of these variables
        # the values do never get mutated -> the evolution stagnates.
        W1 = np.copy(sexy_dino_girl.brain.W1)
        b1 = np.copy(self.brain.b1)
        W2 = np.copy(self.brain.W2)
        b2 = np.copy(sexy_dino_girl.brain.b2)

        # mutate genome
        def mutate(S):
            orig_shape = S.shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    if np.random.random() < self.mutation_rate:
                        S[i,j] += np.random.randn() * 0.5

            return S.reshape(orig_shape)

        W1 = mutate(W1)
        b1 = mutate(b1)
        W2 = mutate(W2)
        b2 = mutate(b2)

        child = Dino()

        # create a small variation in child_brain
        child.brain.W1 = W1
        child.brain.b1 = b1
        child.brain.W2 = W2
        child.brain.b2 = b2

        return child

    def update(self, action):
        # update the dino's state according to the selected action

        # increment dino score
        self.score += 0.2

        # Run
        if action == 0 and not self.is_jumping:
            self.y = 237
            self.width = 59
            self.height = 63

        # Duck
        if action == 1 and not self.is_jumping:
            self.score     -= 0.1 # Punish permanent ducking
            self.height     = 40
            self.width      = 79
            self.y          = 260

        # Jump
        if action == 2:
            self.is_jumping = True

        if self.is_jumping:
            self.score -= 0.5 # Punish permaent jumping
            self.width = 59
            self.height = 63
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= np.power(np.abs(self.jump_count), 1.85) * 0.5 * neg
                self.jump_count -= 0.7
            else:
                self.is_jumping = False
                self.jump_count = 10
                self.width = 59
                self.height = 63
                self.y = 237

    def draw(self, window):

        def reset(self):
            self.is_running = False
            self.is_ducking = False

        # Jumping Animation
        if self.y < 237 or self.is_jumping:
            window.blit(pg.transform.scale(self.img_run[0], (59,63)), (self.x, self.y))

        # Ducking Animation
        if self.y == 260:
            if self.frame_duck >= 16:
                self.frame_duck = 0
            window.blit(pg.transform.scale(self.img_duck[self.frame_duck // 8], (79,40)), (self.x, self.y))
            self.frame_duck += 1

        # Running Animation
        if self.y == 237:
            if self.frame_run >= 16:
                self.frame_run = 0
            window.blit(pg.transform.scale(self.img_run[self.frame_run // 8], (59,63)), (self.x, self.y))
            self.frame_run += 1

        # Draw Dino Hitbox
        pg.draw.rect(window, (41,128,185),
                     (self.x,self.y,self.width,self.height), 1)


        reset(self)
