from abc import ABC
from spaces.discontinuous import DiscontinuousSpace


class DiscontinuousContinuousActionSpace(DiscontinuousSpace, ABC):

    def __init__(self):
        super().__init__()
