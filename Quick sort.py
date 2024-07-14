import pygame, random

pygame.init()

# WINDOW
WINDOW_SIZE = 600
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Sorting Algorithm Visualization')

# VARIABLES
RECT_WIDTH = 20
clock = pygame.time.Clock()
FPS = 10

# COLORS
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# CLASSES
class Rectangle:
    def __init__(self, color, x, height):
        self.color = color
        self.x = x
        self.width = RECT_WIDTH
        self.height = height

    def select(self):
        self.color = BLUE

    def unselect(self):
        self.color = PURPLE

    def set_pivot(self):
        self.color = RED

    def set_sorted(self):
        self.color = GREEN

# FUNCTIONS
def create_rectangles():
    num_rectangles = WINDOW_SIZE // RECT_WIDTH - 5
    rectangles = []
    heights = []

    for i in range(5, num_rectangles):
        height = random.randint(20, 500)
        while height in heights:
            height = random.randint(20, 500)

        heights.append(height)
        rect = Rectangle(PURPLE, i * RECT_WIDTH, height)
        rectangles.append(rect)

    return rectangles

def draw_rects(rectangles):
    WINDOW.fill(YELLOW)

    for rect in rectangles:
        pygame.draw.rect(WINDOW, rect.color, (rect.x, WINDOW_SIZE - rect.height, rect.width, rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x, WINDOW_SIZE), (rect.x, WINDOW_SIZE - rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x + rect.width, WINDOW_SIZE), (rect.x + rect.width, WINDOW_SIZE - rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x, WINDOW_SIZE - rect.height), (rect.x + rect.width, WINDOW_SIZE - rect.height))

def quick_sort(rectangles, low, high):
    if low < high:
        pivot_index = yield from partition(rectangles, low, high)
        yield from quick_sort(rectangles, low, pivot_index - 1)
        yield from quick_sort(rectangles, pivot_index + 1, high)

def partition(rectangles, low, high):
    pivot = rectangles[high]
    pivot.set_pivot()
    draw_rects(rectangles)
    yield
    i = low - 1

    for j in range(low, high):
        rectangles[j].select()
        draw_rects(rectangles)
        yield

        if rectangles[j].height < pivot.height:
            i += 1
            rectangles[i].x, rectangles[j].x = rectangles[j].x, rectangles[i].x
            rectangles[i], rectangles[j] = rectangles[j], rectangles[i]

        rectangles[j].unselect()
        draw_rects(rectangles)
        yield

    rectangles[i + 1].x, rectangles[high].x = rectangles[high].x, rectangles[i + 1].x
    rectangles[i + 1], rectangles[high] = rectangles[high], rectangles[i + 1]

    pivot.unselect()
    rectangles[i + 1].set_sorted()
    draw_rects(rectangles)
    yield

    return i + 1

def display_text(txt, y, size):
    FONT = pygame.font.SysFont('Futura', size)

    text = FONT.render(txt, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE / 2, y))
    WINDOW.blit(text, text_rect)

# MAIN FUNCTION
def main():
    rectangles = create_rectangles()
    draw_rects(rectangles)
    sorting_generator = quick_sort(rectangles, 0, len(rectangles) - 1)

    # MAIN LOOP
    run = True
    sorting = False
    while run:
        clock.tick(FPS)

        if sorting:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw_rects(rectangles)

        display_text('Quick Sort Algorithm Visualization: ', 30, 40)
        display_text('Press SPACE to start/pause sorting and q to quit.', 70, 30)

        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sorting = not sorting
                if event.key == pygame.K_q:
                    run = False

        pygame.display.update()

    pygame.quit()

main()
