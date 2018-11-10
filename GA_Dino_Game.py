import sys
import os
sys.path.append(os.getcwd() + '/' + 'library')

from Dino_Game import *
import Genetic_Algorithm as ga

class GA_Dino_Game(DinoGame):

    def __init__(self, first_init = True):
        super().__init__()

        if first_init == True:
            self.render_flag = False
            self.high_score = []

            # create a new dino population
            self.population_size = 1000
            self.generation = 0
            self.active_dinos, self.all_dinos = ga.create_new_population(self.population_size)

    def step(self):

        def collision_check(dino):
            if len(self.obstacles) != 0:
                obstacle_collided = self.obstacles[0].collide(dino)
                if obstacle_collided:
                    self.active_dinos.pop(self.active_dinos.index(dino))

        # 60 FPS
        if self.render_flag:
            self.clock.tick(self.FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

            key = pg.key.get_pressed()

            # "SPACE" toggles Rendering
            if key[pg.K_SPACE]:
                self.render_flag = not self.render_flag

            # "ESCAPE" closes the Window
            if key[pg.K_ESCAPE]:
                self.close()

        self.increment_counters()
        self.increment_gamespeed()

        # check obstacle collision 3 times! <- pygame bug or implementation bug
        # Only one collision check results in letting some dinos of a population
        # survive obstacle contact, even thought the population is heavily
        # decimated (usually 1 or 2 survive)

        # Check for collisions
        for dino in self.active_dinos:
            collision_check(dino)

        for dino in self.active_dinos:
            collision_check(dino)
            observation = dino.sense_environment(self.obstacles, self.vel)
            action = dino.brain.think_about_action(observation)
            dino.update(action)

        # Check for collisions
        for dino in self.active_dinos:
            collision_check(dino)

        # All Dinos died -> Lets reproduce and generate a new generation!
        if len(self.active_dinos) == 0:

            # increment generation counter
            self.generation += 1

            # Add current gamescore to Highscore list
            self.high_score.append(self.game_score)

            # calcualte fitness for each dino
            self.all_dinos = ga.calculate_fitness(self.all_dinos)

            # create mating pool based on fitness
            dino_mating_pool = []
            dino_mating_pool = ga.create_mating_pool(self.all_dinos)

            self.all_dinos, self.active_dinos = ga.create_next_generation(self.population_size, dino_mating_pool)

            # Reset game environment
            self.reset_game(complete_init_flag = False)

        self.add_obstacle()
        self.update_obstacles()

        if self.render_flag:
            self.add_clouds()
            self.add_ground()
            self.update_ground()
            self.update_clouds()

    def render(self):
        font = pg.font.SysFont('arial', 15)

        if self.render_flag:
            self.window.fill((236,240,241))

            for i in self.grounds:
                i.draw(self.window)

            for i in self.clouds:
                i.draw(self.window)

            for i in self.obstacles:
                i.draw(self.window)

            for i in self.active_dinos:
                i.draw(self.window)

            g_c = font.render('Current Score: ' + str(self.game_score), True, (0,0,0))
            self.window.blit(g_c, (580,10))
            d_a = font.render('Dinos alive : ' + str(len(self.active_dinos)), True, (0,0,0))
            self.window.blit(d_a, (10,10))
            gen = font.render('Generation: ' + str(self.generation), True, (0,0,0))
            self.window.blit(gen, (200,10))
            if len(self.high_score) > 0:
                high = font.render('Total Highscore: ' + str(max(self.high_score)), True, (0,0,0))
                self.window.blit(high, (370,10))

        elif self.speed_counter % 20 == 0:
            a = 135
            b = 285
            self.window.fill((236,240,241))

            bla = font.render('Press SPACE to toggle Game-Rendering (runs faster without)', True, (0,0,0))
            self.window.blit(bla, (b,a))
            gen = font.render('Generation: ' + str(self.generation), True, (0,0,0))
            self.window.blit(gen, (b,a+20))
            if len(self.active_dinos) > 0:
                dino_number = font.render('Dinos alive: ' + str(len(self.active_dinos)), True, (0,0,0))
                self.window.blit(dino_number, (b,a+40))
            g_c = font.render('Current Score: ' + str(self.game_score), True, (0,0,0))
            self.window.blit(g_c, (b,a+60))
            if len(self.high_score) > 0:
                high = font.render('Total Highscore: ' + str(max(self.high_score)), True, (0,0,0))
                self.window.blit(high, (b,a+80))

        pg.display.update()

    def reset_game(self, complete_init_flag):
        self.__init__(first_init = complete_init_flag)

if __name__ == '__main__':
    # main
    env = GA_Dino_Game()
    while True:

        env.step()
        env.render()

    env.close()
