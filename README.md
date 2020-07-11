# Genetic Racer


## Description

My attempt at creating a genetic algorithm that over many generations manages to reach the end of the given track.
  
The algorithm is applied to a population of "cars", that each begins with a set of random vectors or "genes". After each epoch, a new car generation is calculated by randomly reallocating the genes, with a preference to the genes have the best "fitness" (that made the car get furthest in the track). Also, there is a small chance that the genes will mutate, changing the last part of the genes array to random vectors. 
   
The simulation is displayed using p5py and collisions, movement simulation are handled by pumynk physics engine.

Based on the book "The Nature of Code" by  Daniel Shiffman.

#### Technologies

- Python 3.6
- p5py library
- pymunk physics engine

---

## How To Use

Run the racer.py file to run with default parameters, or use addition flags to indicate custom parameters:  
-p \<Population size>  
-m \<Mutation rate>  
-t \<Track file>
  
To add additional walls to the track in real time, press 'l' and start drawing new walls.
  
To see the track used to calculate the fitness of the cars, press 'c'. 

---

## References
 - [Genetic programming wiki](https://en.wikipedia.org/wiki/Genetic_programming)
 - ["The Nature of Code" by Daniel Shiffman](https://natureofcode.com/)
 - [p5py](https://github.com/p5py/p5)
 - [pymunk](http://www.pymunk.org/en/latest/)

---

## Author Info

- [LinkedIn](https://www.linkedin.com/in/tomas-vycas/)