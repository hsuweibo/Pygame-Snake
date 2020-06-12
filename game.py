import random
from snake import Snake
from direction import Direction

"""
This module defines the Game class.
"""


class Game:
    """
    The Game class represents an instance of a snake game.

    Attributes
    ---------
    grid_size: a 2d tuple representing the size of the grid in the game.
    init_head_gpos: a 2d tuple representing the initial position of the snake's head in the grid.
    init_direction: a Direction object representing the initial direction the snake is moving in.
    init_slen: the initial length of the snake.
    snake: a Snake object representing the snake in the game.
    score: the score, representing the number of snack eaten so far.
    snack: a 2d tuple representing the location of the snack on the grid.


    """
    def __init__(self, init_head_gpos, init_direction, init_slen, grid_size):
        """
        Initializes the game. Raises ValueError if init_head_gpos is out of bound wrt grid_size.

        :param init_head_gpos: initial position of the snake's head.
        :param init_direction: initial direction the snake travels in.
        :param init_slen: initial length of the snake.
        :param grid_size: size of the grid.
        """
        if init_head_gpos[0] >= grid_size[0] or init_head_gpos[0] < 0 or \
                init_head_gpos[1] >= grid_size[0] or init_head_gpos[1] < 0:
            raise ValueError("head_gpos should be within the grid.")

        self.grid_size = grid_size
        self.init_head_gpos = init_head_gpos
        self.init_direction = init_direction
        self.init_slen = init_slen
        self.snake = Snake(init_head_gpos, init_direction, init_slen, grid_size)
        self.score = 0
        self.snack = self.get_random_snack_location()

    def get_random_snack_location(self):
        """
        Randomly get a position for the snack on the grid, that does not overlap with the snake's body.

        :return: a 2d tuple representing a position on the grid.
        """
        overlap = True
        while overlap:
            gpos = random.randint(0, self.grid_size[0] - 1), random.randint(0, self.grid_size[1] - 1)
            if gpos not in [snake_pos for snake_pos in self.snake.body]:
                overlap = False

        return gpos

    def is_game_over(self):
        """
        Checks if game is over.

        :return: True iff the head of the snake has collided with other parts of its body.
        """
        return self.snake.head in self.snake.body[1:]

    def has_eaten_snack(self):
        """
        Checks if the snack has been eaten

        :return: True iff the position of the head of the snake overlaps with the position of the snack.
        """
        return self.snake.head == self.snack

    def update_status(self):
        """
        Update the game's status by moving the snake in one unit.

        The function moves the snake, then handles the board state accordingly if the snake hits the snack.
        """
        self.snake.move()
        if self.has_eaten_snack():
            self.snake.grow()
            self.score += 1
            self.snack = self.get_random_snack_location()
        self.snake.update_motion()
        self.snake.update_turning_points()

    def reset(self):
        """
        Resets the game to its initial status, effectively the same as starting a new game.
        """
        self.score = 0
        self.snake = Snake(self.init_head_gpos, self.init_direction, self.init_slen, self.grid_size)
        self.snack = self.get_random_snack_location()

    def print_board_state(self):
        """
        Prints a text representation of the game's state, along with the board's/grid's.

        The function prints a grid using commas. Each cell contains a string S of length 2.
        Each cell by default has the two-space string. If a cell contains the snake's body, then S[1] is a character
        representing the direction that body segment is moving. If that cell contains the head, then the character is
        capitalized. If a cell contains the snack, then S[0] is the character '*'.
        """
        mapping = {Direction.up: 'u', Direction.down: 'd', Direction.right: 'r', Direction.left: 'l'}
        grid = [[None for col in range(self.grid_size[1])] for row in range(self.grid_size[0])]
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
                s = ""
                if (x, y) == self.snack:
                    s += "*"

                if (x, y) in self.snake.body:
                    dir = self.snake.motion[self.snake.body.index((x, y))]

                    if (x, y) == self.snake.head:
                        s += mapping[dir].upper()
                    else:
                        s += mapping[dir]

                grid[y][x] = f"{s:>2}"
        turning_points_str = str(self.snake.turning_points)
        grid_str = '\n'.join([','.join([col for col in row]) for row in grid])
        print(f"{grid_str} \nturning_points: {turning_points_str}")