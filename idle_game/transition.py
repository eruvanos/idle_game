import math
from typing import Callable, Any


class EaseFunctions:

    @staticmethod
    def linear(x: float):
        return x

    @staticmethod
    def sine(x: float):
        return 1 - math.cos((x * math.pi) / 2)


class Transition:
    def __init__(self,
                 *,
                 start,
                 end,
                 attribute,
                 duration: float = 1.0,
                 ease_function=EaseFunctions.sine,
                 delay=0.0,
                 mutation_function: Callable[[Any, str, float], None] = setattr,
                 ):
        """

        :param start: start value
        :param end: target value
        :param attribute: attribute to set
        :param duration: Duration of the transition in seconds
        :param ease_function:
        :param delay: Start transition after x seconds
        :param mutation_function: function to be used to set new value
        """
        self._start = start
        self._end = end
        self._attribute = attribute

        self._duration = duration
        self._elapsed = -delay
        self._ease_function = ease_function
        self._mutation_function = mutation_function

    def update(self, subject, dt):
        self._elapsed += dt
        if self._elapsed > 0:
            progress = self._elapsed / self._duration
            factor = self._ease_function(progress)
            new_value = (self._start + (self._end - self._start) * factor)

            self._mutation_function(subject, self._attribute, new_value)

    @property
    def finished(self):
        return self._elapsed >= self._duration
