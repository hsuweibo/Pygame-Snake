from enum import Enum


class Direction(Enum):
    """An enumerate class representing one of the four directions"""
    up = 1
    down = 2
    left = 3
    right = 4

    @staticmethod
    def is_opposite(dir1, dir2):
        """
        Test to see if dir1 and dir2 are opposite directions.

        :param dir1: a Direction object
        :param dir2: a Direction object
        :return: True iff dir1 and dir2 are opposite.
        """
        accepted = (Direction.up, Direction.down), (Direction.down, Direction.up), (Direction.right, Direction.left)\
            , (Direction.left, Direction.right)

        return (dir1, dir2) in accepted
