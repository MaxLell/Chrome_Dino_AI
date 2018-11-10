import pygame as pg
from Brain import Dino_Brain
import numpy as np
import os

class Dino():

    def __init__(self):

        self.path        = os.getcwd() + '/' + 'sprites' + '/'

        # Image Section
        self.img_run     = [pg.image.load(self.path + 'dino_run_0.png'),
                            pg.image.load(self.path + 'dino_run_1.png')]

        self.img_duck    = [pg.image.load(self.path + 'dino_duck_0.png'),
                            pg.image.load(self.path + 'dino_duck_1.png')]
        self.frame_run    = 0
        self.frame_duck   = 0

        self.color = (41,128,185)

        # Property Section
        self.x           = 50
        self.y           = 237
        self.width       = 59
        self.height      = 63

        self.score = 0
        self.fitness = 0

        # Init Dino Brain
        self.brain = Dino_Brain()

        self.jump_count_const = 8
        self.jump_count_running_variable = self.jump_count_const


        # Dino states
        self.is_running = True
        self.is_ducking = False
        self.is_jumping = False

    def sense_environment(self, obstacles, speed):

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
        observation_dict['dino_y_vel'] = self.jump_count_running_variable / 30

        observation_dict['game_speed'] = speed / 200

        observation = np.array([observation_dict['distance_dino_obstcl_x'],
                                observation_dict['obstcl_y'],
                                observation_dict['dino_y'],
                                observation_dict['dino_y_vel'],
                                observation_dict['game_speed']])

        return observation

    def update(self, action):
        # update the dino's state and score according to the selected action
        # Run
        if action == 0 and not self.is_jumping:
            self.score += 1
            self.y = 237
            self.width = 59
            self.height = 63

        # Duck
        if action == 1 and not self.is_jumping:
            self.score     += 0.3 # Punish permanent ducking
            self.height     = 40
            self.width      = 79
            self.y          = 260

        # Jump
        if action == 2:
            self.is_jumping = True

        if self.is_jumping:
            self.score += 0.1 # Punish permanent jumping
            self.width = 59
            self.height = 63
            if self.jump_count_running_variable >= -self.jump_count_const:
                neg = 1
                if self.jump_count_running_variable < 0:
                    neg = -1
                self.y -= np.power(np.abs(self.jump_count_running_variable), 2) * 0.5 * neg
                self.jump_count_running_variable -= 0.7
            else:
                self.is_jumping = False
                self.jump_count_running_variable = self.jump_count_const
                self.width = 59
                self.height = 63
                self.y = 237

    def draw(self, window):

        def reset(self):
            self.is_running = False
            self.is_ducking = False

        def draw_hitbox(window):
            pg.draw.rect(window, self.color,
                         (self.x,self.y,self.width,self.height), 1)


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
        draw_hitbox(window)


        reset(self)
