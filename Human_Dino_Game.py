#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################ imports #####################

import pygame as pg
import random
import os
import numpy as np


#import dino, obstacles, background

# Globals:
pg.init()

path       = os.getcwd() + '/' + 'Sprites' + '/'

clock      = pg.time.Clock()
disp_x     = 1200
disp_y     = 400

reference  = 237
FPS        = 60

#################### classes ###################

class DinoGame():

    def __init__(self):

        self.iter_counter = 0

        self.score     = 0

        self.timer_enemy_spawn  = 0
        self.speed_counter      = 0
        self.timer_cloud        = 0

        self.obstacles = []
        self.grounds   = []
        self.clouds    = []
        self.vel       = 50
        self.dino      = Dino  (x      = 100,
                                y      = 296,
                                height = 59,
                                width  = 63,
                                path   = path)

        self.observation_dict = {}
        self.observation  = []
        self.reward       = 0
        self.done         = False

        self.observation_space = 3
        self.action_space      = 3

        self.render_init_flag = False

    def reset(self):
        self.__init__()
        return self.curr_observation()

    def action_from_keyboard(self):

        action = 0
        keys = pg.key.get_pressed()

        # ESC pressed? --> terminate program
        if keys[pg.K_ESCAPE]:
            self.dino.alive = False

        elif keys[pg.K_SPACE]:
            action = 2

        elif keys[pg.K_DOWN]:
            action = 1

        else:
            action = 0

        return action

    def add_clouds(self):
        if self.timer_cloud >= random.randrange(200,400):
            rand_y = random.randrange(50,disp_y-220)
            self.clouds.append(Cloud(x = disp_x+70,y = rand_y, vel = 3))
            self.timer_cloud = 0

    def add_ground(self):

        if len(self.grounds) == 0:
            self.grounds.append(Ground(0, reference + 40, self.vel))
            self.grounds.append(Ground(disp_x, reference + 40, self.vel))

        if len(self.grounds) == 1:
            self.grounds.append(Ground(disp_x, reference + 40, self.vel))

    def add_obstacle(self):

        r = random.randrange(0,32)

        # 50% a Ptera-obstacle is spawned, 50% a Cactus-obstacle is spawned
        # the random value is provided to the Cactus to randomly select
        # one cactus obstacle out of 15 different possible cactusses

        if r > 15:
            rand_y = random.randrange(disp_y - 300, disp_y - 180)
            self.obstacles.append(Ptera (x      = disp_x + 70,
                                         y      = rand_y,
                                         vel    = self.vel,
                                         color  = (44,62,80)))


        else:
            self.obstacles.append(Cactus(x      = disp_x + 70,
                                         y      = reference + 59,

                                         vel    = self.vel,
                                         color  = (231,76,60),
                                         rand   = r))

    def move_obstacles(self):
        # move obstacles
        for i in self.obstacles:

            # Move obstacle
            i.move()

            # Check wether obstacle collided with dino
            if self.dino.collide(i):
                self.dino.alive = False

            # remove obstacle once it is off screen
            if i.x < (i.width * -1):
                self.obstacles.pop(self.obstacles.index(i))
                self.reward = 1

    def move_clouds(self):

        for i in self.clouds:

            # Move clouds
            i.move()

            # remove cloud once it is off-screen
            if i.x < (i.width * -1):
                self.clouds.pop(self.clouds.index(i))

    def move_ground(self):

        for i in self.grounds:

            # move ground
            i.move()

            # remove ground once it is off-screen
            if i.x < (i.width * -1):
                self.grounds.pop(self.grounds.index(i))

    def curr_observation(self):

        self.observation_dict['dino_obstcl_distance'] = ((self.obstacles[0].x - self.dino.x)/(1100)) if len(self.obstacles) > 0 else 0
        self.observation_dict['obstcl_y'] = ((self.obstacles[0].y - 100)   / (237 - 100)) if len(self.obstacles) > 0 else 0
        self.observation_dict['dino_y'] = (((self.dino.y - 41.5) / (237 -41.5))-1)*-1


        self.observation = np.array([self.observation_dict['dino_obstcl_distance'],
                                     self.observation_dict['obstcl_y'],
                                     self.observation_dict['dino_y']])

        return self.observation

    def curr_reward(self):

        # distance progress --> no reward
        reward = 0
        # dino alive --> neg. reward
        if self.dino.alive == False:
            reward = -5

        # penalize senseless jumping or ducking:
        if self.dino.is_ducking == True or self.dino.is_jumping == True:
            reward = -0.001


        # passed obstacle --> pos. reward
        # The reward is only given once, when an obstacle has been passed
        if len(self.obstacles) > 0:
            if self.dino.x > (self.obstacles[0].x + self.obstacles[0].width) > (self.dino.x - self.vel):
                reward = 1

        return reward

    def step(self, action):

        """
        action = 0 --> Run
        action = 1 --> Duck
        action = 2 --> Jump
        """

        # Enable: Close Window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.dino.alive = False

        if action == 0 and self.dino.is_jumping == False:
            self.dino.run()

        elif action == 1 and self.dino.is_jumping == False:
            self.dino.duck()

        elif (action == 2 or self.dino.is_jumping == True) and not self.dino.is_ducking:
            self.dino.jump()

        self.move_obstacles()

        # observation
        self.observation = self.curr_observation()

        # reward
        self.reward = self.curr_reward()

        # done
        if self.dino.alive:
            self.done = False
        else:
            self.done = True

        # update enemy timer
        if self.timer_enemy_spawn > random.randrange(60,150):
            self.add_obstacle()
            self.timer_enemy_spawn = 0
        else:
            self.timer_enemy_spawn += 1


        # increase Gamespeed
        if self.speed_counter % 1500 == 0:
            self.vel += 1
            self.speed_counter = 0

        # update cloud_timerr
        self.timer_cloud += 2


        return(self.observation, self.reward, self.done)

    def render(self):

        if self.render_init_flag == False:
            self.render_init_flag = True
            self.window     = pg.display.set_mode((disp_x, disp_y))
            pg.display.set_caption('Dino_game')

        self.add_ground()
        self.add_clouds()

        self.move_clouds()
        self.move_ground()

        # Background
        self.window.fill((236,240,241))

        # Grounds
        for i in self.grounds:
            i.draw(self.window)

        # Clouds
        for i in self.clouds:
            i.draw(self.window)

        # Dino
        self.dino.draw(self.window)

        # Obstacles
        for i in self.obstacles:
            i.draw(self.window)

        # Score
        self.score += 1
        font = pg.font.SysFont('arial', 15)
        text = font.render('Score: ' + str(self.score)[:6], True, (0,0,0))
        self.window.blit(text, (disp_x - 150,10))
        pg.display.update()

    def human_play(self):

        self.reset()

        while self.done == False:

            clock.tick(FPS)
            # step
            action = self.action_from_keyboard()
            obs, rew, done = self.step(action)
            self.render()

    def close(self):
        pg.quit()

# -----------------------------------------------------------------------------

class Cloud():

    def __init__(self, x,y,vel):
        self.x   = x
        self.y   = y
        self.vel = vel
        self.img = pg.image.load(path + 'cloud.png')
        self.width = self.img.get_width()

    def move(self):
        self.x -= self.vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

class Ground():

    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = pg.image.load(path + 'ground.png')

        self.grd_1 = self.img
        self.grd_2 = self.img

        self.width = self.img.get_width()

    def move(self):
        self.x -= self.vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

# -----------------------------------------------------------------------------

class Obstacle(object):
    def __init__(self, x, y, vel, color):
        self.x      = x
        self.y      = y

        self.vel    = vel
        self.color  = color

    def move(self):
        self.x -= self.vel

class Cactus(Obstacle):
    def __init__(self, x, y, vel, color, rand):
        super().__init__(x, y, vel, color)

        self.img  = [pg.image.load(path + 'cactus_' + str(i) + '.png') for i in range(0,16)]
        self.curr_cactus = self.img[rand]

        # compress image size
        self.width  = int(self.curr_cactus.get_width()  * 2/3)
        self.height = int(self.curr_cactus.get_height() * 2/3)
        self.y      = disp_y - 100 - self.height

    def draw(self, window):
        window.blit(pg.transform.scale(self.curr_cactus, (self.width, self.height)), (self.x, self.y))

        pg.draw.rect(window, self.color,
                     (self.x,self.y,self.width,self.height),1)

class Ptera(Obstacle):
    def __init__(self, x, y, vel, color):
        super().__init__(x, y, vel, color)
        self.img     = [pg.image.load(path + 'ptera_0.png'),
                        pg.image.load(path + 'ptera_1.png')]
        self.height  = 53
        self.width   = 61
        self.frame   = 0

    def draw(self, window):
        if self.frame >= 16:
                self.frame = 0
        window.blit(pg.transform.scale(self.img[self.frame // 8], (61,53)), (self.x, self.y))
        self.frame += 1

        pg.draw.rect(window, self.color,
                     (self.x,self.y,self.width,self.height), 1)

# -----------------------------------------------------------------------------

class Dino(object):
    def __init__(self, x, y, height, width, path):
        self.x           = x # specifies the Dino's position in x
        self.y           = y # specifies the Dino's position in y
        self.height      = height # specifies the height of the Dino's hitbox
        self.width       = width # specifies the width of the Dino's hitbox
        self.path        = path

        self.img_run     = [pg.image.load(self.path + 'dino_run_0.png'),
                            pg.image.load(self.path + 'dino_run_1.png')] # contains a list of images of the character animation for running

        self.img_duck    = [pg.image.load(self.path + 'dino_duck_0.png'),
                            pg.image.load(self.path + 'dino_duck_1.png')] # contains a list of images of the cahracter animation for ducking

        self.frame_run     = 0 # contains the current index of the frame to animate for the running animation
        self.frame_duck    = 0 # contains the current index of the frame to animate for the ducking animation

        self.jump_count  = 10

        self.is_jumping  = False # sets the initial is_jumping-flag
        self.is_ducking  = False # sets the initial is_ducking-flag

        self.alive       = True # sets the alive flag for the dino

        self.gravity = 0
        self.vel_y   = 0

    def jump(self):
        self.is_jumping = True

        if self.jump_count >= -10:
            neg = 1
            if self.jump_count < 0:
                neg = -1
            self.y -= np.power(np.abs(self.jump_count), 1.85) * 0.5 * neg
            self.jump_count -= 0.7
        else:
            self.is_jumping = False
            self.jump_count = 10
            self.y = reference

    def duck(self):
        self.is_ducking = True
        self.height     = 40
        self.width      = 79
        self.y          = disp_y - 100 - 40

    def run(self):
        self.is_ducking = False
        self.x = 100
        self.y = disp_y - 100 - 63
        self.width = 59
        self.height = 63

    def collide(self, obstcl):
        if pg.Rect(self.x,
                   self.y,
                   self.width,
                   self.height).colliderect(pg.Rect(obstcl.x,
                                                    obstcl.y,
                                                    obstcl.width,
                                                    obstcl.height)):
            return True
        else:
            return False

    def draw(self, window):
        # Dino jumps -> Draw jumping animation
        if self.is_jumping:
            window.blit(pg.transform.scale(self.img_run[0], (59,63)), (self.x, self.y))

        # Dino ducks -> Draw ducking animation
        if self.is_ducking and not self.is_jumping:
            if self.frame_duck >= 16:
                self.frame_duck = 0
            window.blit(pg.transform.scale(self.img_duck[self.frame_duck // 8], (79,40)), (self.x, self.y))
            self.frame_duck += 1

        # Dino does not jump and does not duck -> Draw normal running animation
        if self.is_ducking == False and self.is_jumping == False:
            if self.frame_run >= 16:
                self.frame_run = 0
            window.blit(pg.transform.scale(self.img_run[self.frame_run // 8], (59,63)), (self.x, self.y))
            self.frame_run += 1


        # Draw Dino Hitbox
        pg.draw.rect(window, (41,128,185),
                     (self.x,self.y,self.width,self.height), 1)

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    env = DinoGame()
    env.human_play()

    env.close()
