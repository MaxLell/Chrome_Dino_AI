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

            self.save_flag = False
            self.save_render_counter = 0
            self.save_draw_flag = False

            self.load_flag = False
            self.load_render_counter = 0
            self.load_draw_flag = False

            self.high_score = []
            self.fittest_dinos = []

            # create a new dino population
            self.population = 150
            self.generation = 0
            self.active_dinos, self.all_dinos = ga.create_new_population(self.population)

    def reset_game(self, complete_init_flag):
        self.__init__(first_init = complete_init_flag)

    def step(self):

        # 60 FPS
        if self.render_flag:
            self.clock.tick(self.FPS)

        # Prevent Window from freezing, when dragging screen
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

            key = pg.key.get_pressed()
            # "SPACE" toggles Rendering
            if key[pg.K_SPACE]:
                if self.render_flag == False:
                    self.render_flag = True
                else:
                    self.render_flag = False
            # "ESCAPE" closes the Window
            if key[pg.K_ESCAPE]:
                self.close()
            # "s" triggers saving the model
            if key[pg.K_s]:
                self.save_flag = True
            # "l" triggers loading the model and
            # generating a population out of it
            if key[pg.K_l]:
                self.load_flag = True

        # increment counters
        self.speed_counter += 1
        self.obstacle_counter += 1
        self.cloud_counter += 1
        self.game_score += 1

        # increase Gamespeed
        if self.speed_counter % 1500 == 0:
            self.vel += 1
            self.speed_counter = 0

        # Add new obstacle
        if self.obstacle_counter == self.obstacle_threshold:
            self.add_obstacle()
            self.obstacle_counter = 0
            self.obstacle_threshold = np.random.randint(40,60)

        # move obstacle
        self.update_obstacles()

        # check obstacle collision 3 times! <- pygame bug or implementation bug
        # Only one collision check results in letting some dinos of a population
        # survive obstacle contact, even thought the population is heavily
        # decimated (usually 1 or 2 survive)

        # 1. Collision Check
        if len(self.obstacles) != 0:
            for obstacle in self.obstacles:
                for dino in self.active_dinos:
                    obstacle_collided = obstacle.collide(dino)
                    if obstacle_collided:
                        self.active_dinos.pop(self.active_dinos.index(dino))

        for dino in self.active_dinos:

            # 2. Collision Check
            dino_collided = dino.collide(self.obstacles)

            if dino_collided:
                self.active_dinos.pop(self.active_dinos.index(dino))

            # Dinos sense enviroment
            observation = dino.sense_environment(self.obstacles)

            # Dinos think about what they've seen and select an action
            action = dino.think(observation)

            # Dinos act
            dino.update(action)

            # 3. Collision Check
            if len(self.obstacles) != 0:
                for obstacle in self.obstacles:
                    for dino in self.active_dinos:
                        obstacle_collided = obstacle.collide(dino)
                        if obstacle_collided:
                            self.active_dinos.pop(self.active_dinos.index(dino))

        # All Dinos died -> Lets reproduce and generate a new generation!
        if len(self.active_dinos) == 0:
            # increment generation counter
            self.generation += 1

            # Add current gamescore to Highscore list
            self.high_score.append(self.game_score)

            # Reset game environment
            self.reset_game(complete_init_flag = False)

            # calcualte fitness for each dino
            self.all_dinos = ga.calculate_fitness(self.all_dinos)

            # create mating pool based on fitness
            dino_mating_pool = []
            dino_mating_pool = ga.create_mating_pool(self.all_dinos)

            # Add fittest Dino to the fittest_dino_list
            self.fittest_dinos.append(dino_mating_pool[0])

            # mate and set up the next generation!
            self.all_dinos, self.active_dinos = ga.create_next_generation(self.population, dino_mating_pool)

        if len(self.high_score) > 0:

            # Meteor:
            # Mass extinction - The previous population did never get fit enough
            # lets bring in the meteor!! + create a new population, which is propably
            # fitter - if not ... well you know the game
            # 30% of the populations do not evolve over longer periods of time
            # --> Threshold at 80 generations.
            if max(self.high_score) < 10000 and self.generation >= 80:

                # Reset game environment and
                # generates a completly new population
                self.reset_game(complete_init_flag = True)

            # Want to save the best model?
            if self.save_flag:
                self.save_flag = False
                self.save_model()
                self.save_draw_flag = True
                self.save_render_counter = 100

        # Want to load the previously saved model?
        if self.load_flag:
            self.load_flag = False
            self.load_model()
            self.load_draw_flag = True
            self.load_render_counter = 100

    def render(self):
        font = pg.font.SysFont('arial', 15)
        self.window.fill((236,240,241))
        if self.render_flag:

            # Rendering Screen
            if self.cloud_counter == self.cloud_threshold:
                self.add_clouds()
                self.cloud_threshold = np.random.randint(70,120)
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
            g_c = font.render('Current Score: ' + str(self.game_score), True, (0,0,0))
            self.window.blit(g_c, (580,10))
            d_a = font.render('Dinos alive : ' + str(len(self.active_dinos)), True, (0,0,0))
            self.window.blit(d_a, (10,10))
            gen = font.render('Generation: ' + str(self.generation), True, (0,0,0))
            self.window.blit(gen, (200,10))
            if len(self.high_score) > 0:
                high = font.render('Total Highscore: ' + str(max(self.high_score)), True, (0,0,0))
                self.window.blit(high, (370,10))
        else:
            # No Rendering Screen
            bla = font.render('Press SPACE to toggle Game-Rendering (faster without)', True, (0,0,0))
            a = 135
            b = 285
            self.window.blit(bla, (b,a))
            g_c = font.render('Current Score: ' + str(self.game_score), True, (0,0,0))
            self.window.blit(g_c, (b,a+20))
            gen = font.render('Generation: ' + str(self.generation), True, (0,0,0))
            self.window.blit(gen, (b,a+40))
            if len(self.high_score) > 0:
                high = font.render('Total Highscore: ' + str(max(self.high_score)), True, (0,0,0))
                self.window.blit(high, (b,a+60))

        # Print Successful Save
        if self.save_draw_flag or self.save_render_counter > 0:
            self.save_draw_flag = False
            self.save_render_counter -= 1
            txt_save = font.render('Best Dino saved', True, (0,0,0))
            self.window.blit(txt_save, (10, 320))

        # Print Successful Load
        if self.load_draw_flag or self.load_render_counter > 0:
            self.load_draw_flag = False
            self.load_render_counter -= 1
            txt_load = font.render('Best Previous Dino loaded', True, (0,0,0))
            self.window.blit(txt_load, (600, 320))

        pg.display.update()

    def save_model(self):
        apex_dino_properties = {}

        # The best of the fittest Dinos of each Generation
        apex_dino = sorted(self.fittest_dinos, key = lambda dino: dino.fitness)[::-1][0]

        apex_dino_properties['W1'] = apex_dino.brain.W1
        apex_dino_properties['b1'] = apex_dino.brain.b1
        apex_dino_properties['W2'] = apex_dino.brain.W2
        apex_dino_properties['b2'] = apex_dino.brain.b2

        np.save('save/apex_dino.npy', apex_dino_properties)

    def load_model(self):
        self.reset_game(True)

        apex_dino_properties = np.load('save/apex_dino.npy')[()]

        for dino in self.all_dinos:
            dino.brain.W1 = apex_dino_properties['W1']
            dino.brain.b1 = apex_dino_properties['b1']
            dino.brain.W2 = apex_dino_properties['W2']
            dino.brain.b2 = apex_dino_properties['b2']

        for dino in self.active_dinos:
            dino.brain.W1 = apex_dino_properties['W1']
            dino.brain.b1 = apex_dino_properties['b1']
            dino.brain.W2 = apex_dino_properties['W2']
            dino.brain.b2 = apex_dino_properties['b2']

if __name__ == '__main__':
    # main
    env = GA_Dino_Game()
    while True:

        env.step()
        env.render()

    env.close()
