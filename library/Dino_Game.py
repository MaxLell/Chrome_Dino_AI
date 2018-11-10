import pygame as pg
import random
import os
import numpy as np
from sys import exit

from Dino import *
from Obstacles import *
from Background import *

class DinoGame():

    def __init__(self):

        # Set screen parameters
        pg.init()
        self.disp_x = 800
        self.disp_y = 350
        self.FPS        = 60
        pg.display.set_caption('Dino_game')
        self.window     = pg.display.set_mode((self.disp_x, self.disp_y))
        self.window_color = (247,247,247)
        self.clock      = pg.time.Clock()

        self.game_score = 0

        # game incrementors
        self.cloud_counter    = 60
        self.cloud_threshold    = np.random.randint(60,100)
        self.obstacle_counter = 0
        self.obstacle_threshold = np.random.randint(40,60)
        self.speed_counter = 0

        # game object lists
        self.obstacles  = []
        self.grounds    = []
        self.clouds     = []

        # Gamespeed
        self.vel        = 15

        self.add_obstacle()

    def add_clouds(self):

        if self.cloud_counter == self.cloud_threshold:
            self.clouds.append(Cloud())
            self.cloud_threshold = np.random.randint(70,120)
            self.cloud_counter = 0

    def add_ground(self):

        if len(self.grounds) == 0:
            self.grounds.append(Ground(0, self.vel))
            self.grounds.append(Ground(self.disp_x, self.vel))

        if len(self.grounds) == 1:
            self.grounds.append(Ground(self.disp_x, self.vel))

    def add_obstacle(self):

        # Add new obstacle
        if self.obstacle_counter == self.obstacle_threshold:

            r = random.randrange(0,4)
            if r < 2:
                self.obstacles.append(Cactus(vel = self.vel))
            else:
                self.obstacles.append(Ptera (vel = self.vel))

            self.obstacle_counter = 0
            self.obstacle_threshold = np.random.randint(40,80)

    def update_obstacles(self):
        # update obstacles
        for i in self.obstacles:

            # update obstacle
            i.update()

            # remove obstacle once it is off screen
            if i.x < (i.width * -1):
                self.obstacles.pop(self.obstacles.index(i))
                self.reward = 1

    def update_clouds(self):

        for i in self.clouds:

            # update clouds
            i.update()

            # remove cloud once it is off-screen
            if i.x < (i.width * -1):
                self.clouds.pop(self.clouds.index(i))

    def update_ground(self):

        for i in self.grounds:

            # move ground
            i.update()

            # remove ground once it is off-screen
            if i.x < (i.width * -1):
                self.grounds.pop(self.grounds.index(i))

    def increment_counters(self):
        # increment counters
        self.speed_counter += 1
        self.obstacle_counter += 1
        self.cloud_counter += 1

        if self.speed_counter % 4 == 0:
            self.game_score += 1

    def increment_gamespeed(self):
        # increase Gamespeed
        if self.speed_counter % 1000 == 0:
            self.vel += 2
            self.speed_counter = 0

    def step(self):
        pass

    def render(self):
        pass

    def close(self):

        pg.display.quit()
        pg.quit()
        print('Current score:',self.game_score)
        exit()
