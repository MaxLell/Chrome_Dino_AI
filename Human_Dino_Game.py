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

        # Prevent Window from freezing, when dragging screen
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

        # increment counters
        self.speed_counter += 1
        self.obstacle_counter += 1
        self.cloud_counter += 1
        self.game_score += 1

        # increase Gamespeed
        if self.speed_counter % 1000 == 0:
            self.vel += 1
            self.speed_counter = 0

        # Add new obstacle
        if self.obstacle_counter == self.obstacle_threshold:
            self.add_obstacle()
            self.obstacle_counter = 0
            self.obstacle_threshold = np.random.randint(40,60)

        # move obstacle
        self.update_obstacles()

        action = self.action_from_keyboard()

        self.dino.update(action)

        for obstacle in self.obstacles:
            obstacle_collided = obstacle.collide(self.dino)
            if obstacle_collided:
                self.close()

        self.game_score += 1

    def render(self):

        # Background
        self.window.fill((236,240,241))

        # Grounds
        self.add_ground()
        self.update_ground()

        for i in self.grounds:
            i.draw(self.window)

        # Clouds
        if self.cloud_counter == self.cloud_threshold:
            self.add_clouds()
            self.cloud_threshold = np.random.randint(70,120)
            self.cloud_counter = 0

        self.update_clouds()

        for i in self.clouds:
            i.draw(self.window)

        # Obstacles
        for i in self.obstacles:
            i.draw(self.window)

        # Dino
        self.dino.draw(self.window)

        # Score
        self.game_score += 1
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
