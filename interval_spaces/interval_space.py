from abc import ABC, abstractmethod
from gym.spaces.space import Space


class IntervalSpace(Space, ABC):
    """ Interface for interval action spaces"""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def add(self, *args):
        raise NotImplementedError

    @abstractmethod
    def  remove(self, *args):
        raise NotImplementedError

    @abstractmethod
    def contains(self, x):
        raise NotImplementedError

    @abstractmethod
    def intervals(self):
        raise NotImplementedError
