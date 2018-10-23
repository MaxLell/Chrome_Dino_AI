# Dino_Ai
Reinforcement Learning via Neuro-Evolution.
The Chrome Dino Game learns to play itself and to avoid the obstacles beyond human capabilities. If you want further explanation, please feel free to visit [my article on Medium](https://medium.com/@maximilian.lell/neuro-evolution-with-dinosaurs-1cfce5eadbd8)

## Overview
This package contains two versions of Google Chrome's famous Dino Game.

1. One Version can be played by Humans (Run `Human_Dino_Game.py`). You can compare yourself with the trained model.
2. The other version trains and plays itself by Reinforcement Learning (Run `GA_Dino_Game.py`). Its core algorithm is based on Neuro-Evolution Algorithms (Genetic Algorithms applied on Neural Networks - more Info in "Sources")

## Usage

__Human-playable-version__ `Human_Dino_Game.py`:
- Press __"SPACE"__ to jump over an obstacle
- Press __"KEYDOWN"__ to duck under a Ptera dinosaur.

The game ends automatically once you got hit.


__Genetic-algorithm-version__ `GA_Dino_game.py`:
- Press __"s"__ to save the dino with the best score so far. The files are stored in the `/save` folder.
- Press __"l"__ to load a previously saved model. By default the package is provided with a pretrained Dino that you can load (max score 19000).
- Press __"SPACE"__ to toggle the visualisation. By deactivating the visualisation the code runs faster and therefore the Dinos evolve faster, to obtain higher scores.

## Dependencies:

- Python 3.6.3
- Numpy 1.13.3
- Pygame 1.9.4

## Sources:

- Google - Game Concept
- Deeplearning.ai
- The [Code Bullet Youtube Channel](https://youtu.be/sB_IGstiWlc)
- ["The Nature of Code"](https://natureofcode.com/book/chapter-9-the-evolution-of-code/) + YouTube Series about applied [Neuro-Evolution Algorithms](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6Yd3975YwxrR0x40XGJ_KGO)
