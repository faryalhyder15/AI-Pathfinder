import pygame
import random
import time
import heapq
from collections import deque

# Basic grid and window configuration
ROWS, COLS = 20, 20
CELL_SIZE = 20
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Start and goal positions
START = (0, 0)
TARGET = (19, 19)

# Probability for random obstacles appearing during search
DYNAMIC_OBSTACLE_PROB = 0.05

# Depth limit used by DLS
DEPTH_LIMIT = 30

TITLE = "GOOD PERFORMANCE TIME APP"

# Movement directions (clockwise with diagonals)
MOVES = [
    (-1, 0),    # up
    (0, 1),     # right
    (1, 1),     # down-right
    (1, 0),     # down
    (0, -1),    # left
    (-1, -1),   # up-left
]

# Color definitions for visualization
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
PURPLE = (160, 32, 240)
GRAY = (200, 200, 200)


class Grid:
    """
    Represents the environment.
    Keeps track of static and dynamic obstacles.
    """

    def __init__(self):
        self.walls = set()
        self.dynamic_walls = set()

    def in_bounds(self, r, c):
        """Check if a cell is inside the grid."""
        return 0 <= r < ROWS and 0 <= c < COLS

    def is_blocked(self, cell):
        """Check if a cell is blocked by any obstacle."""
        return cell in self.walls or cell in self.dynamic_walls

    def spawn_dynamic_wall(self):
        """
        Randomly add obstacles during search to simulate a dynamic environment.
        """
        if random.random() < DYNAMIC_OBSTACLE_PROB:
            cell = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            if cell not in (START, TARGET) and cell not in self.walls:
                self.dynamic_walls.add(cell)


def neighbors(grid, node):
    """
    Generate valid neighboring cells based on movement rules.
    """
    for dr, dc in MOVES:
        nr, nc = node[0] + dr, node[1] + dc
        if grid.in_bounds(nr, nc):
            yield (nr, nc)


def bfs(grid, start, goal):
    """
    Breadth-First Search using a queue.
    Explores level by level.
    """
    queue = deque([start])
    parent = {start: None}
    explored = []

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == goal:
            break

        grid.spawn_dynamic_wall()

        for nxt in neighbors(grid, current):
            if nxt not in parent and not grid.is_blocked(nxt):
                parent[nxt] = current
                queue.append(nxt)

    return reconstruct_path(parent, start, goal), explored


def dfs(grid, start, goal):
    """
    Depth-First Search using a stack.
    Reversing neighbors preserves the intended move order.
    """
    stack = [start]
    parent = {start: None}
    explored = []

    while stack:
        current = stack.pop()
        explored.append(current)

        if current == goal:
            break

        grid.spawn_dynamic_wall()

        for nxt in reversed(list(neighbors(grid, current))):
            if nxt not in parent and not grid.is_blocked(nxt):
                parent[nxt] = current
                stack.append(nxt)

    return reconstruct_path(parent, start, goal), explored


def ucs(grid, start, goal):
    """
    Uniform Cost Search.
    Always expands the least-cost node first.
    """
    pq = [(0, start)]
    parent = {start: None}
    cost = {start: 0}
    explored = []

    while pq:
        _, current = heapq.heappop(pq)
        explored.append(current)

        if current == goal:
            break

        grid.spawn_dynamic_wall()

        for nxt in neighbors(grid, current):
            if grid.is_blocked(nxt):
                continue

            diagonal = abs(nxt[0] - current[0]) == 1 and abs(nxt[1] - current[1]) == 1
            step_cost = 1.414 if diagonal else 1
            new_cost = cost[current] + step_cost

            if nxt not in cost or new_cost < cost[nxt]:
                cost[nxt] = new_cost
                parent[nxt] = current
                heapq.heappush(pq, (new_cost, nxt))

    return reconstruct_path(parent, start, goal), explored


def dls(grid, start, goal, limit):
    """
    Depth-Limited Search.
    DFS with a depth cutoff.
    """
    stack = [(start, 0)]
    parent = {start: None}
    explored = []

    while stack:
        current, depth = stack.pop()
        explored.append(current)

        if current == goal:
            break
        if depth == limit:
            continue

        grid.spawn_dynamic_wall()

        for nxt in reversed(list(neighbors(grid, current))):
            if nxt not in parent and not grid.is_blocked(nxt):
                parent[nxt] = current
                stack.append((nxt, depth + 1))

    return reconstruct_path(parent, start, goal), explored


def iddfs(grid, start, goal):
    """
    Iterative Deepening DFS.
    Repeatedly runs DLS with increasing depth limits.
    """
    explored_total = []

    for depth in range(ROWS * COLS):
        path, explored = dls(grid, start, goal, depth)
        explored_total.extend(explored)

        if path:
            return path, explored_total

    return [], explored_total


def bidirectional(grid, start, goal):
    """
    Bidirectional search.
    Runs BFS simultaneously from start and goal.
    """
    q1, q2 = deque([start]), deque([goal])
    p1, p2 = {start: None}, {goal: None}
    explored = []

    while q1 and q2:
        a = q1.popleft()
        b = q2.popleft()
        explored.extend([a, b])

        grid.spawn_dynamic_wall()

        for nxt in neighbors(grid, a):
            if nxt not in p1 and not grid.is_blocked(nxt):
                p1[nxt] = a
                q1.append(nxt)
                if nxt in p2:
                    return merge_paths(p1, p2, nxt), explored

        for nxt in neighbors(grid, b):
            if nxt not in p2 and not grid.is_blocked(nxt):
                p2[nxt] = b
                q2.append(nxt)
                if nxt in p1:
                    return merge_paths(p1, p2, nxt), explored

    return [], explored


def reconstruct_path(parent, start, goal):
    """Rebuild path from goal to start using parent links."""
    if goal not in parent:
        return []

    path = []
    current = goal
    while current:
        path.append(current)
        current = parent[current]

    return path[::-1]


def merge_paths(p1, p2, meet):
    """Merge paths from bidirectional search."""
    path1 = []
    current = meet
    while current:
        path1.append(current)
        current = p1[current]
    path1.reverse()

    path2 = []
    current = p2[meet]
    while current:
        path2.append(current)
        current = p2[current]

    return path1 + path2


def draw(screen, grid, explored, path):
    """Draw grid, explored nodes, obstacles, and final path."""
    screen.fill(WHITE)

    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, GRAY,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
            )

    for cell in explored:
        pygame.draw.rect(
            screen, BLUE,
            (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    for cell in grid.walls | grid.dynamic_walls:
        pygame.draw.rect(
            screen, BLACK,
            (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    for cell in path:
        pygame.draw.rect(
            screen, PURPLE,
            (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    pygame.draw.rect(
        screen, GREEN,
        (START[1] * CELL_SIZE, START[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )
    pygame.draw.rect(
        screen, RED,
        (TARGET[1] * CELL_SIZE, TARGET[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )

    pygame.display.update()
    time.sleep(0.05)


def run(algorithm):
    """Main driver function."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    grid = Grid()

    if algorithm == "bfs":
        path, explored = bfs(grid, START, TARGET)
    elif algorithm == "dfs":
        path, explored = dfs(grid, START, TARGET)
    elif algorithm == "ucs":
        path, explored = ucs(grid, START, TARGET)
    elif algorithm == "dls":
        path, explored = dls(grid, START, TARGET, DEPTH_LIMIT)
    elif algorithm == "iddfs":
        path, explored = iddfs(grid, START, TARGET)
    else:
        path, explored = bidirectional(grid, START, TARGET)

    for i in range(len(explored)):
        draw(screen, grid, explored[:i + 1], [])

    for i in range(len(path)):
        draw(screen, grid, explored, path[:i + 1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == "__main__":
    run("bfs")   # bfs | dfs | ucs | dls | iddfs | bi
