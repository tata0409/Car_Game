## This program is a game that will be used to train a machine 
The game is made on pygame. It is simple, there are 4 color coded squares, there's a hotel on one of them and a passenger on another one of them. The goal is to transport the passenger to the hotel. 
To train the machine to learn how to transport the passenger most efficiently we will use reinforcement learning, more specifically Q-learning.
We have to files: "main.py" - the game with the car being controlled by a real human, and "main_ML.py" - version of the game where a machine controls the car.
The ML version is a simplified version of the game with no requirement to pick up the passanger.