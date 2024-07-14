import pygame
import random
import heapq

pygame.init()

# WINDOW
WINDOW_SIZE = 600
GRID_SIZE = 20
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Dijkstra Algorithm Visualization')

# VARIABLES
clock = pygame.time.Clock()
FPS = 10

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)

# CLASSES
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.color = WHITE
        self.neighbors = []
        self.distance = float('inf')
        self.previous = None

    def __lt__(self, other):
        return self.distance < other.distance

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(WINDOW, GRAY, (self.x, self.y, GRID_SIZE, GRID_SIZE), 1)

    def add_neighbors(self, grid):
        if self.row < len(grid) - 1 and not isinstance(grid[self.row + 1][self.col], Obstacle):
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not isinstance(grid[self.row - 1][self.col], Obstacle):
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < len(grid[0]) - 1 and not isinstance(grid[self.row][self.col + 1], Obstacle):
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not isinstance(grid[self.row][self.col - 1], Obstacle):
            self.neighbors.append(grid[self.row][self.col - 1])

class Obstacle(Node):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color = BLACK

def make_grid(rows, cols, start, target):
    grid = [[Node(i, j) for j in range(cols)] for i in range(rows)]
    for _ in range(rows * cols // 5):  # Add obstacles randomly
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        grid[row][col] = Obstacle(row, col)
    grid[start[0]][start[1]] = Node(start[0], start[1])
    grid[target[0]][target[1]] = Node(target[0], target[1])
    for row in grid:
        for node in row:
            node.add_neighbors(grid)
    return grid

def draw_grid(grid):
    WINDOW.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    pygame.display.update()

def reconstruct_path(current_node):
    while current_node:
        current_node.color = PURPLE
        draw_grid(grid)
        current_node = current_node.previous
        yield

def dijkstra(grid, start_node, target_node):
    start_node.distance = 0
    pq = [(0, start_node)]
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        current_node.color = BLUE
        draw_grid(grid)
        yield

        if current_node == target_node:
            current_node.color = GREEN
            draw_grid(grid)
            yield from reconstruct_path(current_node)
            return

        for neighbor in current_node.neighbors:
            if neighbor in visited:
                continue
            new_distance = current_distance + 1  # Each move has a cost of 1
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous = current_node
                heapq.heappush(pq, (new_distance, neighbor))

        current_node.color = YELLOW
        draw_grid(grid)
        yield

    for row in grid:
        for node in row:
            if node in visited:
                node.color = GREEN
    draw_grid(grid)

def display_text(txt, y, size):
    FONT = pygame.font.SysFont('Futura', size)
    text = FONT.render(txt, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE / 2, y))
    WINDOW.blit(text, text_rect)

# MAIN FUNCTION
def main():
    rows = cols = WINDOW_SIZE // GRID_SIZE
    start = (0, 0)
    target = (rows - 1, cols - 1)
    grid = make_grid(rows, cols, start, target)
    start_node = grid[start[0]][start[1]]
    target_node = grid[target[0]][target[1]]
    start_node.color = RED
    target_node.color = RED
    draw_grid(grid)

    dijkstra_generator = dijkstra(grid, start_node, target_node)

    run = True
    searching = False
    while run:
        clock.tick(FPS)

        if searching:
            try:
                next(dijkstra_generator)
            except StopIteration:
                searching = False
        else:
            draw_grid(grid)

        display_text('Dijkstra Algorithm Visualization: ', 30, 40)
        display_text('Press SPACE to start/pause Dijkstra and q to quit.', 70, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    searching = not searching
                if event.key == pygame.K_q:
                    run = False

        pygame.display.update()

    pygame.quit()

main()
