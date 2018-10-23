import pygame as pg
import random
import os

class Environment():

    def __init__(self):
        self.path = os.getcwd() + '/' + 'sprites' + '/'

    def update(self):
        self.x -= self.vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class Cloud(Environment):

    def __init__(self):
        super().__init__()
        self.x   = 830
        self.y   = random.randrange(50,180)
        self.vel = 3
        self.img = pg.image.load(self.path + 'cloud.png')
        self.width = self.img.get_width()

class Ground(Environment):

    def __init__(self, x, vel):
        super().__init__()
        self.x = x
        self.y = 277
        self.vel = vel
        self.img = pg.image.load(self.path + 'ground.png')
        self.width = self.img.get_width()
