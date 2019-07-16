# Planet Protector Pygame

Another space shooter - based on the Kids Can Code tutorials, with some of my own bits sprinkled in. It started mostly as a my 7 year old wanted to learn how to code. You know, dads and kids toys.

This is a work in progress.

** Current status **
* Basic levels working
* Single planet and double planets
* Slower and faster astroids
* Single and double bullet guns
* You gets hit it is game over
* Your planet gets hit it is game over
* Most sounds

![Screen Shot](https://raw.githubusercontent.com/yohanswanepoel/planet_protector_pygame/master/demo/Untitled%202.png)

Technical bits
* Class based break-out of actors
* Settings file that is somewhat ignored at the moment

** To Do **
* UI features
* Score saving ect
* Settings saving changing
* Adding shields
* Adding damage 

** How to Run **
* create a python environment
* `pip install -r requirements.py`
* `python smhup.py`

** Structure of Code **
* Actors are in the ./actors folder if you want to change images or behaviour start there
* Scene control is in smhup.py
* I tried to avoid global variables to make pieces more reusable
