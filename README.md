# Genetic Racer
## Description

My attempt at creating a [genetic algorithm]((https://en.wikipedia.org/wiki/Genetic_programming)) that over several generations manages to reach the end of the given track.
  
The algorithm is applied to a population of cars. Each car has a set of random vectors or "genes" that are used as a set of small forces that move the car on the map. After all of the cars in the simulation have finished their movements or hit the wall, a new generation of the population of cars is generated, and the simulation restarts. This process finishes once one of the cars reaches the finish line at the end of the track loop.

The new generations are calculated in 4 steps: fitness calculation, fitness proportionate member selection, crossover, and mutation (mutated cars are drawn in red).

The simulation is displayed using [p5py](https://github.com/p5py/p5). Collisions and movement simulations are handled by [pymunk](http://www.pymunk.org/en/latest/) physics engine.

Based on the book "The Nature of Code" by  Daniel Shiffman.



---

## Technologies

- Python 3.6
- [p5py](https://github.com/p5py/p5)
- [pymunk](http://www.pymunk.org/en/latest/) physics engine
- [Shapely](https://pypi.org/project/Shapely/)

---
## Screenshots
### Visual indicators

The cars drawn in red carry "genes" that have mutated over the last generation.

The small yellow dots indicate 5 furthest points the cars have ever reached.

  <p align="left">
    <img src="../screenshots/1.png" alt="search" width="500" style="padding-left: 10px"/>
    <img src="../screenshots/2.png" alt="search" width="500" style="padding-left: 10px"/>
    <img src="../screenshots/3.png" alt="search" width="500" style="padding-left: 10px"/>
    <img src="../screenshots/4.png" alt="search" width="500" style="padding-left: 10px"/>
  </p>

---

## How To Use

Run the racer.py file to run with default parameters, or use addition flags to indicate custom parameters:  
-p \<Population size>  
-m \<Mutation rate from 0 to 100>  
-mf \<Map file>
  
To add additional walls to the track in real-time, press 'l' and start drawing new walls.
  
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
