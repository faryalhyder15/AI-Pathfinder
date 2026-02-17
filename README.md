# AI-Pathfinder
AI Uninformed Search in a Grid Environment Code

###  Course Information
Course: AI 2002 – Artificial Intelligence (Spring 2026)  
Assignment: 1 – Uninformed Search Visualization  
Student Name: Faryal Jafferi and Rida Mehmood 
Roll no: 23F-0606 and 23F-0554

## Project Overview

This project implements an AI Pathfinder that visualizes how different **Uninformed (Blind) Search Algorithms** explore a grid environment.
The system navigates from a **Start Point (S)** to a **Target Point (T)** while avoiding:
- Static walls
- Dynamically spawning obstacles

The GUI animates how each algorithm explores nodes step-by-step, showing:

- Frontier nodes  
- Explored nodes  
- Final path  
- Dynamic obstacle appearance  


##  Implemented Algorithms

The following six uninformed search algorithms are implemented:

1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. Uniform Cost Search (UCS)
4. Depth-Limited Search (DLS)
5. Iterative Deepening DFS (IDDFS)
6. Bidirectional Search


##  Movement Rules

Nodes are expanded in strict clockwise order:

1. Up
2. Right
3. Down-Right (Diagonal)
4. Down
5. Left
6. Up-Left (Diagonal)

Movement includes diagonal transitions.


##  Dynamic Environment

During execution:

- A dynamic obstacle may randomly appear at each step.
- If a new obstacle blocks a path, the algorithm adapts accordingly.
- Start and Target nodes are never blocked.

Dynamic obstacle probability is configurable.


##  GUI Features

- Real-time visualization using Pygame
- Step-by-step animation
- Different colors for:
  - Start node (Green)
  - Target node (Red)
  - Explored nodes (Blue)
  - Final path (Purple)
  - Obstacles (Black)
- Animated exploration effect with slight delay

---

## ⚙️ Requirements

Install dependencies before running:

