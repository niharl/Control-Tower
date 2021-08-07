# Control-Tower
A Pygame replica of the Android/iOS <a href = "https://play.google.com/store/apps/developer?id=Bojan+Skaljac&hl=en_GB&gl=US"> Control Tower </a>game

## Set-up
This version of Tetris runs on Python 3.8 and Pygame 2.0. 

To install Pygame, run the following command in the terminal:

```
pip3 install pygame
```

To run, simply run the "control tower.py" file.

## Gameplay
Aircraft randomly appear at edges of the screen.  As the game progresses, the frequency with which new aircraft appear increases.  The task is to draw paths guiding aircraft to the runways and helipad whilst avoiding collisions.  To create a landing path, click on an aicraft/helicopter and draw a path.  If the path turns white, this means that the path will lead to a landing. If it remains red, then the aircraft will continue flying in a straight line after it has completed the path.  Aircraft are automatically deflected back into the centre if they reach the edge of the screen.

Your score is the number of aircraft succesfully landed.  If a collision occurs, the game ends.

## Interface screenshots

## Authors
* **Nihar Lohan** - June 2020
