from abc import ABC
from gym.spaces.space import Space


class IntervalSpace(Space, ABC):

    def __init__(self):
        super().__init__()
