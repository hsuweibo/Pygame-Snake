from direction import Direction


class Snake:
    """
    A class representing a snake.

    Attributes
    -----------
    grid_size: a 2d tuple representing the size of the grid.
    body: an ordered list of 2d tuples representing the positions of all the snake's body.
        The head is at the front of the list and the tail is at the end of the list.
    slen: the length of the snake's body.
    head: same as self.body[0]
    motion: an ordered list of Direction representing the direction each segment in self.body will move next time.
    last_head_motion: a Direction object representing the direction of the head before the last time the snake moves.
    turning_points: a dictionary of 2d tuples to Direction objects. Each key-val pair represents a position, and
    direction in which a segment of the snake's body needs to turn, if the segment enters the position.
    """

    def __init__(self, head_gpos, direction, slen, grid_size):
        """
        Initializes a linear snake. Raises ValueError if head_gpos is out of bound.

        :param head_gpos: the position of the snake's head on the grid.
        :param direction: the direction the snake is moving in.
        :param slen: the length of the snake's body.
        :param grid_size: the size of the grid.
        """
        if head_gpos[0] >= grid_size[0] or head_gpos[0] < 0 or head_gpos[1] >= grid_size[0] or head_gpos[1] < 0:
            raise ValueError("head_gpos should be within the grid.")

        self.grid_size = grid_size
        self.body = self.__create_body(head_gpos, direction, slen)
        self.slen = len(self.body)
        self.head = self.body[0]
        # We set all segments of the snake's body to be removing in the same direction.
        self.motion = [direction for i in range(self.slen)]
        self.last_head_motion = self.motion[0]
        self.turning_points = dict()

    def __create_body(self, head_gpos, direction, slen):
        """
        Creates a linear snake.

        The length of the snake will be adjusted. If slen is too large, the snake hits itself immediately and
        is thus pointless. For this reason, slen is set to be at most the distance from head_gpos to the
        boundary of the grid.

        :param head_gpos: position of the head.
        :param direction: direction the snake is moving in.
        :param slen: the length of the snake.
        :return: a list of ordered 2d tuple representing the position of each segment of the snake's body.
        """
        if direction is Direction.up:
            slen = min(slen, self.grid_size[1] - head_gpos[1])
            body = [(head_gpos[0], head_gpos[1] + i) for i in range(slen)]
        elif direction is Direction.down:
            slen = min(slen, 1 + head_gpos[1] - 0)
            body = [(head_gpos[0], head_gpos[1] - i) for i in range(slen)]
        elif direction is Direction.left:
            slen = min(slen, self.grid_size[0] - head_gpos[0])
            body = [(head_gpos[0] + i, head_gpos[1]) for i in range(slen)]
        elif direction is Direction.right:
            slen = min(slen, 1 + head_gpos[0] - 0)
            body = [(head_gpos[0] - i, head_gpos[1]) for i in range(slen)]

        return body

    def move(self):
        """
        Moves the snake by one unit according to the direction the snake is moving in.
        """
        def compute_new_gpos(gpos, dir):
            """
            Given a position and direction, compute the new position after moving in that direction.

            :param gpos: initial position.
            :param dir: a Direction object.
            :return: the new position.
            """
            new_gpos_x = gpos[0]
            new_gpos_y = gpos[1]
            if dir is Direction.up:
                new_gpos_y -= 1
            elif dir is Direction.down:
                new_gpos_y += 1
            elif dir is Direction.left:
                new_gpos_x -= 1
            elif dir is Direction.right:
                new_gpos_x += 1

            if new_gpos_x < 0:
                new_gpos_x = self.grid_size[0] - 1
            if new_gpos_x >= self.grid_size[0]:
                new_gpos_x = 0

            if new_gpos_y < 0:
                new_gpos_y = self.grid_size[1] - 1
            if new_gpos_y >= self.grid_size[1]:
                new_gpos_y = 0

            return new_gpos_x, new_gpos_y

        for i in range(self.slen):
            self.body[i] = compute_new_gpos(self.body[i], self.motion[i])

        self.head = self.body[0]

    def update_motion(self):
        """Updates the direction in which each segment of the body is moving.

        This method is to be called after self.move().
        """
        for i, gpos in enumerate(self.body):
            if gpos in self.turning_points:
                self.motion[i] = self.turning_points[gpos]

        self.last_head_motion = self.motion[0]

    def update_turning_points(self):
        """Updates the turning points.

        This method is to be called after self.update_motion()
        """
        # If the tail of the snake is in a position where a turn needs to occur, then remove the turning point, because
        # all other segments of the snake has already "passed" the turning point.
        last_gpos = self.body[self.slen - 1]
        if last_gpos in self.turning_points:
            del self.turning_points[last_gpos]

    def grow(self):
        """Grow the snake by adding one segment to the snake's tail.
        """
        new_gpos = self.body[self.slen - 1]
        dir = self.motion[self.slen - 1]
        if dir is Direction.up:
            new_gpos = new_gpos[0], new_gpos[1] + 1
        elif dir is Direction.down:
            new_gpos = new_gpos[0], new_gpos[1] - 1
        elif dir is Direction.left:
            new_gpos = new_gpos[0] + 1, new_gpos[1]
        elif dir is Direction.right:
            new_gpos = new_gpos[0] - 1, new_gpos[1]

        self.body += [new_gpos]
        self.motion += [dir]
        self.slen += 1

    def change_direction(self, new_dir):
        """
        Changes the direction the snake's head is travelling to new_dir.
        :param new_dir: a Direction object.
        """
        # The snake cannot move in an opposite direction. If the direction does not changes, do nothing.
        if not Direction.is_opposite(self.last_head_motion, new_dir) and new_dir is not self.last_head_motion:
            self.motion[0] = new_dir
            self.turning_points[self.head] = new_dir

    def __str__(self):
        """
        Returns a string representation of the snake.
        """
        body_str = str(self.body)
        motion_str = str(self.motion)
        turning_points_str = str(self.turning_points)
        return f'body: {body_str} \nmotion: {motion_str} \nturning_points: {turning_points_str}'
