# 2048 Game & AI player implemented in Python

The objective of the game slide numbered tiles on a grid to combine them to create a tile with the number 2048. The original game is written using Javascript and CSS but my version is implemented in Python. The game also has AI player that can play the game for you. [Demo](./src/demo.gif)

## Install The Game
1. git clone https://github.com/wensu425/2048-Game-AI.git
2. cd 2048-Game-AI
3. python 2048.py
PS: the game needs pygame & numpy to run. If you don't have the two packages install in your computer, you need to run "pip install pygame" & "pip install numpy"


## User mannual
1. Hit the "enter" key to start AI mode and hit "enter" key again to stop AI mode
2. Use arrow keys to move tiles

## AI Methodology

The computer is view as a chance player who randomly pick an empty slot and place 2-tile and the AI player is a max player.

The AI player will construct a game tree from any state of the game (like the tree you see in the slides). The tree depth is designed to be three which represents all the game states of a player-computer-player sequence (the player makes a move, the computer place a tile, and then the player makes another move). After growing the tree, Compute the expectimax values of all the nodes in the game tree, and return the optimal move for the player. 

## Reference

[Base-Game-Engine](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2)