# Dino_Ai
AI learns to play Google Chrome Dinosaur Game with a Genetic Algorithm.

Overview
============
This package contains two Versions of Google Chrome's famous Dino Game.


1. One Version can be played by Humans (Run Human_Dino_Game.py).
2. The other version trains and plays itself by Reinforcement Learning (Run GA_Dino_Game.py). Its core algorithm is based on Neuro-Evolution Algorithms (Genetic Algorithms applied on Neural Networks).


You can save and load a model. Initially the package is provided with a save-File, which lets the best Dino run to a max score of approximantly 70000 (apex_dino.npy). Press "l" to load the previously saved model. If you want to train and save your own version press "s" to save the fittest Dino of all generations (overwrites the previous saved version).

Dependencies:
============
- numpy
- Pygame

Sources:
============
- Google - Game Concept
- Deeplearning.ai
- The Code Bullet Youtube Channel (https://youtu.be/sB_IGstiWlc)
- "The Nature of Code" - See Chapter 9: Genetic Algorithms + YouTube Series about applied Neuro-Evolution Algorithms (https://www.youtube.com/playlist?list=PLRqwX-V7Uu6Yd3975YwxrR0x40XGJ_KGO)
