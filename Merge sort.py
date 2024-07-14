import pygame
import random

pygame.init()

# WINDOW
WINDOW_SIZE = 600
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Merge Sort Visualization')

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

    def set_color(self, color):
        self.color = color

# FUNCTIONS
def create_rectangles():
    num_rectangles = WINDOW_SIZE // RECT_WIDTH
    rectangles = []

    for i in range(num_rectangles):
        height = random.randint(20, 500)
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

def merge_sort(rectangles):
    if len(rectangles) > 1:
        mid = len(rectangles) // 2
        left_half = rectangles[:mid]
        right_half = rectangles[mid:]

        yield from merge_sort(left_half)
        yield from merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            left_half[i].set_color(BLUE)
            right_half[j].set_color(RED)
            draw_rects(rectangles)
            yield

            if left_half[i].height < right_half[j].height:
                rectangles[k] = left_half[i]
                left_half[i].set_color(GREEN)
                i += 1
            else:
                rectangles[k] = right_half[j]
                right_half[j].set_color(GREEN)
                j += 1
            k += 1

        while i < len(left_half):
            left_half[i].set_color(GREEN)
            rectangles[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            right_half[j].set_color(GREEN)
            rectangles[k] = right_half[j]
            j += 1
            k += 1

        for rect in rectangles:
            rect.set_color(PURPLE)

        draw_rects(rectangles)
        yield

def display_text(txt, y, size):
    FONT = pygame.font.SysFont('Futura', size)
    text = FONT.render(txt, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE / 2, y))
    WINDOW.blit(text, text_rect)

# MAIN FUNCTION
def main():
    rectangles = create_rectangles()
    draw_rects(rectangles)
    sorting_generator = merge_sort(rectangles)

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

        display_text('Merge Sort Visualization: ', 30, 40)
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
