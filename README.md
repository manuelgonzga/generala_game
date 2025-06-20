# Concurrent Simulation of the Generala Dice Game

This project is a **simulation of the dice game Generala**, implemented in **Python 3**, 
using **multithreading** to run and compare the performance of different playing strategies. 
It was developed as part of an academic assignment in collaboration with classmates.

---

## Project Overview

The program simulates thousands of Generala matches using four different strategies:

- **Intelligent**: Evaluates probabilities to make optimal decisions.
- **Greedy**: Always picks the highest immediate scoring option.
- **Immediate Score**: Chooses based on instant scoring, without planning ahead.
- **Random**: Makes entirely random choices (used as a control baseline).

Each strategy is executed **concurrently** in its own thread. Once the simulation ends, the program outputs each strategy’s **average, max, min score**, and **execution time**.

---

## Requirements

- Python 3.6 or higher  
- No external libraries needed (`threading`, `random`, `collections`, `time`)

---

## How to Run

1. Download or clone the `Generala.py` file.
2. In the terminal, run:

   ```bash
   python Generala.py
