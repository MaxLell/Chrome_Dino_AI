import pygame as pg
import random
import os
import numpy as np
from sys import exit

from dino import *
from obstacles import *
from background import *
import genetic_algorithm as ga

class DinoGame():

    def __init__(self, first_init = True):

        self.game_score = 0

        self.cloud_counter    = 0
        self.obstacle_counter = 0
        self.obstacle_threshold = np.random.randint(70,90)
        self.speed_counter = 0

        self.obstacles  = []
        self.grounds    = []
        self.clouds     = []

        self.vel        = 15

        self.population = 100

        self.add_obstacle()

        if first_init == True:
            pg.init()

            # Screen resolution and window title
            self.disp_x     = 800
            self.disp_y     = 350
            self.FPS        = 60
            pg.display.set_caption('Dino_game')
            self.window     = pg.display.set_mode((self.disp_x, self.disp_y))

            self.clock      = pg.time.Clock()

            self.high_score = []

            # create dino population
            self.generation = 0
            self.active_dinos, self.all_dinos = ga.create_new_population(self.population)

    def reset_game(self):
        self.__init__(first_init = False)

    def add_clouds(self):
        self.clouds.append(Cloud())

    def add_ground(self):

        if len(self.grounds) == 0:
            self.grounds.append(Ground(0, self.vel))

            self.grounds.append(Ground(1200, self.vel))

        if len(self.grounds) == 1:
            self.grounds.append(Ground(1200, self.vel))

    def add_obstacle(self):
        r = random.randrange(0,3)
        if r < 2:
            self.obstacles.append(Cactus(vel = self.vel))
        else:
            self.obstacles.append(Ptera (vel = self.vel))

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

    def step(self):

        # 60 FPS
        self.clock.tick(60)

        # Prevent Window from freezing, when dragging screen
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

        # increment counters
        self.speed_counter += 1
        self.obstacle_counter += 1
        self.cloud_counter += 1
        self.game_score += 1

        # Add new obstacle
        if self.obstacle_counter == self.obstacle_threshold:
            self.add_obstacle()
            self.obstacle_counter = 0
            self.obstacle_threshold = np.random.randint(40,60)

        # increase Gamespeed
        if self.speed_counter % 1500 == 0:
            self.vel += 1
            self.speed_counter = 0

        # move obstacle
        self.update_obstacles()

        # check obstacle collision multiple times! <- pygame bug
        # or implementation bug

        # 1. Collsion Check
        if len(self.obstacles) != 0:
            for obstacle in self.obstacles:
                for dino in self.active_dinos:
                    obstacle_collided = obstacle.collide(dino)
                    if obstacle_collided:
                        self.active_dinos.pop(self.active_dinos.index(dino))


        for dino in self.active_dinos:

            # 2. Collsion Check
            dino_collided = dino.collide(self.obstacles)

            if dino_collided:
                self.active_dinos.pop(self.active_dinos.index(dino))

            # Dinos sense enviroment
            observation = dino.sense_environment(self.obstacles)

            # Dinos think about what they've seen and select an action
            action = dino.think(observation)

            # Dinos act
            dino.update(action)

            # 3. Collsion Check
            if len(self.obstacles) != 0:
                for obstacle in self.obstacles:
                    for dino in self.active_dinos:
                        obstacle_collided = obstacle.collide(dino)
                        if obstacle_collided:
                            self.active_dinos.pop(self.active_dinos.index(dino))


        # All Dinos died -> Lets reproduce and generate a new generation!
        if len(self.active_dinos) == 0:

            # Add current gamescore to Highscore list
            self.high_score.append(self.game_score)

            # Reset game environment
            self.reset_game()

            # calcualte fitness for each dino
            self.all_dinos = ga.calculate_fitness(self.all_dinos)

            # create mating pool based on fitness
            dino_mating_pool = []
            dino_mating_pool = ga.create_mating_pool(self.all_dinos)

            # mate and set up the next generation!
            self.all_dinos, self.active_dinos = ga.create_next_generation(self.population, dino_mating_pool)

            # increment genaration counter
            self.generation += 1

    def render(self):
        # Background
        self.window.fill((236,240,241))

        if (self.cloud_counter % 100) == 0:
            self.add_clouds()
            self.cloud_counter = 0

        self.add_ground()

        self.update_clouds()
        self.update_ground()

        # Grounds
        for i in self.grounds:
            i.draw(self.window)

        # Clouds
        for i in self.clouds:
            i.draw(self.window)

        # Obstacles
        for i in self.obstacles:
            i.draw(self.window)

        # Dinos
        for i in self.active_dinos:
            i.draw(self.window)

        # high_score

        font = pg.font.SysFont('arial', 15)
        g_c = font.render('Current Score: ' + str(self.game_score), True, (0,0,0))
        self.window.blit(g_c, (580,10))
        d_a = font.render('Dinos alive : ' + str(len(self.active_dinos)), True, (0,0,0))
        self.window.blit(d_a, (10,10))
        gen = font.render('Generation: ' + str(self.generation), True, (0,0,0))
        self.window.blit(gen, (200,10))
        if len(self.high_score) > 0:
            high = font.render('Total Highscore: ' + str(max(self.high_score)), True, (0,0,0))
            self.window.blit(high, (370,10))

        pg.display.update()

    def close(self):

        pg.display.quit()
        pg.quit()
        exit()

if __name__ == '__main__':
    # main
    env = DinoGame()
    while True:

        env.step()
        env.render()

    env.close()
