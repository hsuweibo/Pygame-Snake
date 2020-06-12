import random
from snake import Snake
from direction import Direction


class Game:
    def __init__(self, init_head_gpos, init_direction, init_slen, grid_size):
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
        overlap = True
        while overlap:
            gpos = random.randint(0, self.grid_size[0] - 1), random.randint(0, self.grid_size[1] - 1)
            if gpos not in [snake_pos for snake_pos in self.snake.body]:
                overlap = False

        return gpos

    def is_game_over(self):
        return self.snake.head in self.snake.body[1:]

    def has_eaten_snack(self):
        return self.snake.head == self.snack

    def update_status(self):
        self.snake.move()
        if self.has_eaten_snack():
            self.snake.grow()
            self.score += 1
            self.snack = self.get_random_snack_location()
        self.snake.update_motion()
        self.snake.update_turning_points()

    def reset(self):
        self.score = 0
        self.snake = Snake(self.init_head_gpos, self.init_direction, self.init_slen, self.grid_size)
        self.snack = self.get_random_snack_location()

    def print_board_state(self):
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