from enum import Enum


class Topic(Enum):
    """
    An enumeration representing different topics
    """

    ENGLISH = "English"
    MATH = "Math"

    @staticmethod
    def from_value(value):
        for topic in Topic:
            if topic.value == value:
                return topic
