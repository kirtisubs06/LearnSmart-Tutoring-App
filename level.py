from enum import Enum


class Level(Enum):
    """
    An enumeration representing different difficulty levels for the lessons.
    """

    EASY = "Easy"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

    @staticmethod
    def from_value(value):
        for level in Level:
            if level.value == value:
                return level