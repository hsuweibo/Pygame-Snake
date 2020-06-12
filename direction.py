from enum import Enum


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4

    @staticmethod
    def is_opposite(dir1, dir2):
        accepted = (Direction.up, Direction.down), (Direction.down, Direction.up), (Direction.right, Direction.left)\
            , (Direction.left, Direction.right)

        return (dir1, dir2) in accepted
