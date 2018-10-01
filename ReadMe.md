# Dino_Ai
Reinforcement Learning via Neuro-Evolution.
The Chrome Dino Game learns to play itself and to avoid the obstacles beyond human capabilities.

## Overview

This package contains two versions of Google Chrome's famous Dino Game.

1. One Version can be played by Humans (Run `Human_Dino_Game.py`).
2. The other version trains and plays itself by Reinforcement Learning (Run `GA_Dino_Game.py`). Its core algorithm is based on Neuro-Evolution Algorithms (Genetic Algorithms applied on Neural Networks - more Info in "Sources")

## Usage

__Human-playable-version__ `Human_Dino_Game.py`:
- Press __"SPACE"__ to jump over an obstacle
- Press __"KEYDOWN"__ to duck under a Ptera dinosaur
The game ends automatically once you got hit.


__Genetic-algorithm-version__ `GA_Dino_game.py`:
- Press __"s"__ to save the dino with the best score so far. The files are stored in the `/save` folder.
- Press __"l"__ to load a previously saved model. By default the package is provided with a pretrained Dino that you can load (score 110000).
- Press __"SPACE"__ to toggle the visualisation. By deactivating the visualisation the code runs faster and therefore the Dinos evolve faster, to obtain higher scores.

The current population of the programm consists of 150 different Dinos. It might happen that it takes many generations until these evolve to surpass the 10000 score-mark. Therefore, if the score at generation 80 is lower then 10000 the game resets itself with a completly new population ("__Meteor - Event__"). This usually occurs in 3 / 10 cases. This stagnation could be avoided by increasing the population to at least 1000, but the code gets very slow, by doing so.

Usually the game learns to play itself up to a score of 70000. To compare the human performance vs the machine performance the `Human_Dino_Game.py` can be run.

## Dependencies:

- numpy
- Pygame

## Sources:

- Google - Game Concept
- Deeplearning.ai
- The Code Bullet Youtube Channel (https://youtu.be/sB_IGstiWlc)
- "The Nature of Code" - See Chapter 9: Genetic Algorithms + YouTube Series about applied Neuro-Evolution Algorithms (https://www.youtube.com/playlist?list=PLRqwX-V7Uu6Yd3975YwxrR0x40XGJ_KGO)
