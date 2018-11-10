import sys
import os
sys.path.append(os.getcwd() + '/' + 'library')

from Dino_Game import *
from Dino import *

class Human_Dino_Game(DinoGame):

    def __init__(self):
        super().__init__()

        self.dino = Dino()

    def action_from_keyboard(self):

        action = 0
        keys = pg.key.get_pressed()

        # ESC pressed? --> terminate program
        if keys[pg.K_ESCAPE]:
            self.close()

        # Jump
        elif keys[pg.K_SPACE]:
            action = 2

        # Duck
        elif keys[pg.K_DOWN]:
            action = 1

        # Run
        else:
            action = 0

        return action

    def step(self):

        self.clock.tick(self.FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

        self.increment_counters() 
        self.increment_gamespeed()

        self.add_clouds()
        self.add_obstacle()
        self.add_ground()

        self.update_obstacles()
        self.update_ground()
        self.update_clouds()

        # read action from keyboard
        action = self.action_from_keyboard()

        # act
        self.dino.update(action)

        # Collision checks
        for obstacle in self.obstacles:
            obstacle_collided = obstacle.collide(self.dino)
            if obstacle_collided:
                self.close()

    def render(self):

        # Background
        self.window.fill((236,240,241))

        # Grounds
        for i in self.grounds:
            i.draw(self.window)

        # Clouds
        for i in self.clouds:
            i.draw(self.window)

        # Obstacles
        for i in self.obstacles:
            i.draw(self.window)

        # Dino
        self.dino.draw(self.window)

        # Score
        font = pg.font.SysFont('arial', 15)
        text = font.render('Score: ' + str(self.game_score), True, (0,0,0))
        self.window.blit(text, (580,10))

        pg.display.update()

if __name__ == '__main__':
    # main
    env = Human_Dino_Game()

    while True:

        env.step()
        env.render()

    env.close()
