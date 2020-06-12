import tkinter
import tkinter.messagebox
import pygame
from game import Game
from direction import Direction

# Customizable constants. These can be changed.
GRID_WIDTH = 500
GRID_HEIGHT = 500
CELL_WIDTH = 20  # Width of the square cells in the grid.
SNAKE_COLOR = (20, 252, 78)
SNACK_COLOR = (255, 249, 161)
GRID_BORDER_COLOR = (255, 255, 255)
CELL_OUTLINE_COLOR = (64, 64, 64)
TEXT_COLOR = (255, 255, 255)

# Customizable margins.
# It is best to not change top margin and text size because the top margin is adjusted to be able to hold the game text.
TEXT_SIZE = 30
LEFT_MARGIN = 30
RIGHT_MARGIN = 30
TOP_MARGIN = 100
BOTTOM_MARGIN = 30

# Derived constants.
GRID_SIZE = GRID_WIDTH//CELL_WIDTH, GRID_HEIGHT//CELL_WIDTH
WINDOW_WIDTH = LEFT_MARGIN + GRID_WIDTH + RIGHT_MARGIN
WINDOW_HEIGHT = TOP_MARGIN + GRID_HEIGHT + BOTTOM_MARGIN

pygame.init()
display = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("Snake Game")


def ask_for_retry(game):
    print("collided")
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    reply = tkinter.messagebox.askyesno("Game over", f"Your score is {game.score}. Play again? Select no to quit.")
    try:
        root.destroy()
    except:
        pass

    return reply


def update_display(game):
    display.fill((0, 0, 0))
    draw_snack(game.snack)
    draw_snake(game.snake)
    draw_grid()
    draw_score(game)
    pygame.display.update()


def color_cell(gpos, color):
    rect = pygame.Rect(LEFT_MARGIN + gpos[0] * CELL_WIDTH, TOP_MARGIN + gpos[1] * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
    pygame.draw.rect(display, color, rect)


def draw_snake(snake):
    for gpos in snake.body:
        color_cell(gpos, SNAKE_COLOR)


def draw_snack(snack):
    color_cell(snack, SNACK_COLOR)


def draw_grid():
    pygame.draw.rect(display, GRID_BORDER_COLOR, pygame.Rect(LEFT_MARGIN, TOP_MARGIN, GRID_WIDTH, GRID_HEIGHT), 2)
    for row in range(GRID_SIZE[0]):
        pygame.draw.line(display, CELL_OUTLINE_COLOR, (LEFT_MARGIN, TOP_MARGIN + row * CELL_WIDTH),
                         (LEFT_MARGIN + GRID_WIDTH, TOP_MARGIN + row * CELL_WIDTH))

    for col in range(GRID_SIZE[1]):
        pygame.draw.line(display, CELL_OUTLINE_COLOR, (LEFT_MARGIN + col * CELL_WIDTH, TOP_MARGIN),
                         (LEFT_MARGIN + col * CELL_WIDTH, TOP_MARGIN + GRID_HEIGHT))


def draw_score(game):
    font = pygame.font.SysFont("cambria", TEXT_SIZE)
    surface = font.render(f"Score: {game.score:0>2}", True, TEXT_COLOR)
    size = surface.get_size()
    display.blit(surface, (LEFT_MARGIN, (TOP_MARGIN - size[1]) // 2))


def main():
    game = Game((GRID_SIZE[0]//2, GRID_SIZE[1]//2), Direction.right, 10, GRID_SIZE)
    running = True
    update_display(game)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.snake.change_direction(Direction.left)
                elif event.key == pygame.K_UP:
                    game.snake.change_direction(Direction.up)
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction(Direction.down)
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction(Direction.right)

        if running:
            game.update_status()
            update_display(game)
            if game.is_game_over():
                if ask_for_retry(game):
                    game.reset()
                else:
                    running = False

            # Putting the delay between display update and next iter of event handling makes the key response crispier
            pygame.time.delay(75)


if __name__ == '__main__':
    main()
