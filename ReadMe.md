# Dino_Ai
Reinforcement Learning via Neuro-Evolution.
The Chrome Dino Game learns to play itself and to avoid the obstacles beyond human capabilities.

## Overview
This package contains two versions of Google Chrome's famous Dino Game.

1. One Version can be played by Humans (Run `Human_DinoGame.py`). You can compare yourself with the trained model.
2. The other version trains and plays itself by Reinforcement Learning (Run `AI_DinoGame.py`). Its core algorithm is based on Neuro-Evolution Algorithms (Genetic Algorithms applied on Neural Networks - more Info in "Sources")

## Usage

__Human-playable-version__ `Human_DinoGame.py`:
- Press __"SPACE"__ to jump over an obstacle
- Press __"KEYDOWN"__ to duck under a Ptera dinosaur.

The game ends automatically once you got hit.


__Genetic-algorithm-version__ `AI_DinoGame.py`:
- Press __"SPACE"__ to toggle the visualisation. By deactivating the visualisation the code runs much faster and therefore the Dinos evolve faster.

## Dependencies:

- Python 3.6.3
- Numpy 1.13.3
- Pygame 1.9.4

## Sources:

- [my article on Medium](https://medium.com/@maximilian.lell/neuro-evolution-with-dinosaurs-1cfce5eadbd8)
- Google - Game Concept
- Deeplearning.ai
- The [Code Bullet Youtube Channel](https://youtu.be/sB_IGstiWlc)
- ["The Nature of Code"](https://natureofcode.com/book/chapter-9-the-evolution-of-code/) + YouTube Series about applied [Neuro-Evolution Algorithms](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6Yd3975YwxrR0x40XGJ_KGO)
