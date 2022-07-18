from abc import ABC
from spaces.discontinuous import DiscontinuousSpace


class DiscontinuousDiscreteActionSpace(DiscontinuousSpace, ABC):

    def __init__(self):
        super().__init__()
