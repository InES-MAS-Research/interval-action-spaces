from abc import ABC
from gym.spaces.space import Space


class DiscontinuousSpace(Space, ABC):

    def __init__(self):
        super().__init__()
