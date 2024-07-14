import pygame
import random

pygame.init()

# WINDOW
WINDOW_SIZE = 600
GRID_SIZE = 20
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('DFS Algorithm Visualization')

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

# CLASSES
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GRID_SIZE
        self.y = row * GRID_SIZE
        self.color = WHITE
        self.neighbors = []
        self.visited = False

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

def dfs(grid, start_node, target_node):
    stack = [start_node]

    while stack:
        current_node = stack.pop()
        if current_node.visited:
            continue
        current_node.visited = True

        current_node.color = BLUE
        draw_grid(grid)
        yield

        if current_node == target_node:
            current_node.color = GREEN
            draw_grid(grid)
            return

        for neighbor in current_node.neighbors:
            if not neighbor.visited:
                stack.append(neighbor)
        
        current_node.color = YELLOW
        draw_grid(grid)
        yield

    for row in grid:
        for node in row:
            if node.visited:
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

    dfs_generator = dfs(grid, start_node, target_node)

    run = True
    searching = False
    while run:
        clock.tick(FPS)

        if searching:
            try:
                next(dfs_generator)
            except StopIteration:
                searching = False
        else:
            draw_grid(grid)

        display_text('DFS Algorithm Visualization: ', 30, 40)
        display_text('Press SPACE to start/pause DFS and q to quit.', 70, 30)

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
