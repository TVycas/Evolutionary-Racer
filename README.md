# Genetic Racer
## Description

My attempt at creating a genetic algorithm that over a number of generations manages to reach the end of the given track.
  
The algorithm is applied to a population of cars. Each car has a set of random vectors or "genes" that are used as a set of small forces that move the car in the map. After all of the cars in the simulation have finished their movements or hit the wall, a new generation of the population of cars is generated and the simulation restarts. This process finishes once one of the cars reaches the finish line at the end of the track loop.

The new generations are calculated in 4 steps: fitness calculation, member selection, crossover, and mutation. You can find more information about these operations [here](https://en.wikipedia.org/wiki/Genetic_programming).
   
The simulation is displayed using [p5py](https://github.com/p5py/p5). Collisions and movement simulations are handled by [pymunk](http://www.pymunk.org/en/latest/) physics engine.

Based on the book "The Nature of Code" by  Daniel Shiffman.

---

#### Technologies

- Python 3.6
- [p5py](https://github.com/p5py/p5)
- [pymunk](http://www.pymunk.org/en/latest/) physics engine
- [Shapely](https://pypi.org/project/Shapely/)

---

## Screenshots



---

## How To Use

Run the racer.py file to run with default parameters, or use addition flags to indicate custom parameters:  
-p \<Population size>  
-m \<Mutation rate from 0 to 100>  
-mf \<Map file>
  
To add additional walls to the track in real time, press 'l' and start drawing new walls.
  
To see the checkpoints used to calculate the fitness of the cars, press 'c'. 

---

## References
 - [Genetic programming wiki](https://en.wikipedia.org/wiki/Genetic_programming)
 - ["The Nature of Code" by Daniel Shiffman](https://natureofcode.com/)
 - [p5py](https://github.com/p5py/p5)
 - [pymunk](http://www.pymunk.org/en/latest/)

---

## Author Info

- [LinkedIn](https://www.linkedin.com/in/tomas-vycas/)