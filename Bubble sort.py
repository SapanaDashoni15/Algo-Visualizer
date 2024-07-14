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

def bubble_sort(rectangles):
    num_rectangles = len(rectangles)

    for i in range(num_rectangles):
        for j in range(0, num_rectangles - i - 1):
            rectangles[j].select()
            rectangles[j + 1].select()
            draw_rects(rectangles)
            
            if rectangles[j].height > rectangles[j + 1].height:
                rectangles[j].x, rectangles[j + 1].x = rectangles[j + 1].x, rectangles[j].x
                rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
            
            rectangles[j].unselect()
            rectangles[j + 1].unselect()
            draw_rects(rectangles)
            yield
        
        rectangles[num_rectangles - i - 1].set_sorted()
        draw_rects(rectangles)

    for rect in rectangles:
        rect.set_sorted()
    draw_rects(rectangles)

def display_text(txt, y, size):
    FONT = pygame.font.SysFont('Futura', size)

    text = FONT.render(txt, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE / 2, y))
    WINDOW.blit(text, text_rect)

# MAIN FUNCTION
def main():
    rectangles = create_rectangles()
    draw_rects(rectangles)
    sorting_generator = bubble_sort(rectangles)

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

        display_text('Bubble Sort Algorithm Visualization: ', 30, 40)
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
