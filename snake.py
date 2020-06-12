from direction import Direction


class Snake:
    def __init__(self, head_gpos, direction, slen, grid_size):
        if head_gpos[0] >= grid_size[0] or head_gpos[0] < 0 or head_gpos[1] >= grid_size[0] or head_gpos[1] < 0:
            raise ValueError("head_gpos should be within the grid.")

        self.grid_size = grid_size
        self.body = self.__create_body(head_gpos, direction, slen)
        self.slen = len(self.body)
        self.head = self.body[0]
        self.motion = [direction for i in range(self.slen)]
        # stores the motion of the head, before the last call to self.move(). This is needed in self.change_direction().
        self.last_head_motion = self.motion[0]
        self.turning_points = dict()

    def __create_body(self, head_gpos, direction, slen):
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
        def compute_new_gpos(gpos, dir):
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
        for i, gpos in enumerate(self.body):
            if gpos in self.turning_points:
                self.motion[i] = self.turning_points[gpos]

        self.last_head_motion = self.motion[0]

    def update_turning_points(self):
        last_gpos = self.body[self.slen - 1]
        if last_gpos in self.turning_points:
            del self.turning_points[last_gpos]

    def grow(self):
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
        if not Direction.is_opposite(self.last_head_motion, new_dir) and new_dir is not self.last_head_motion:
            self.motion[0] = new_dir
            self.turning_points[self.head] = new_dir

    def __str__(self):
        body_str = str(self.body)
        motion_str = str(self.motion)
        turning_points_str = str(self.turning_points)
        return f'body: {body_str} \nmotion: {motion_str} \nturning_points: {turning_points_str}'
