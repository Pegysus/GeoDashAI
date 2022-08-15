# GeoDashAI

Utilizing Deep Q Learning to teach an AI how to play the computer/mobile platformer game Geometry Dash. This project uses pygame as the game engine for the geometry dash game mechanics and Tensorflow to create and train the Q-learning neural network to play the game.

## About This Project

GeoDashAI is a project I made to become accustomed to the Tensorflow library in creating neural networks. GeoDashAI is coded in only python and uses pygame to create the game as a whole, from the sprites to the map. The game itself is a very simplified version of Geometry Dash and only uses the core mechanics of the game to train the AI. This includes the side-scrolling aspect of the game, a jump/rotation mechanic, and platforms and spikes that could "kill" the player. The game only has one level with different obstacles to train the AI in different scenarios.

For the neural network, GeoDashAI utilizes Tensorflow's vast library to construct a deep Q-learning NN to effectively train the data. Q-learning is a good option for learning this game and games in general because of model-free natural. By not requiring a previously built model, the learning algorithm can quickly learn from the rewards in the environment (how long the player lasts in the level). To see the environment, I took inspriation from Daniel Slater's PyGamePlayer which overrides pygame's environment and allows a player (or in this case, the AI) to view the game and send commands (actions such as jumping) to "play" the game.

## Getting Started

### Dependencies

* Python version 3.7+
* Python Libraries:
    * pygame v2.1.2
    * Tensorflow v2.9.1
    * numpy v1.21.0
    * Pillow v9.2.0
* macOS 10.9 or later
* Windows 7 or later

### Installation

* To clone the project, run
```
git clone https://github.com/Pegysus/GeoDashAI.git
```
* Once cloned, install all dependencies used in the project
    * Make sure you have the latest version of pip installed. To install pip click [here](https://pip.pypa.io/en/stable/installation/), or to upgrade your current version of pip, run the command ```pip install --upgrade pip```
    * To install dependencies run ```pip install -r requirements.txt``` (Using IDE's such as PyCharm may allow you to automatically install any necessary libraries needed for a project. In that case, you can run that instead of pip install)

To run the project, locate and run the main.py file in the main folder.

## Version History

* 0.1
    * Initial Release

## Acknowledgements

Code inspiration, code snippits, etc.

* [PyGamePlayer](https://github.com/DanielSlater/PyGamePlayer/tree/b4889a7f98606892db0907d60459e553681ac53c)
* [CodeBullet](https://www.youtube.com/c/CodeBullet)
