from tests import test_interval_space
from interval_spaces.bucket_space import BucketSpace


class AVLTreeTest(test_interval_space.TestIntervalSpaces):

    tree = BucketSpace(0.0, 1.0)

    def test_insert_intervals(self):
        pass

    def test_order_intervals(self):
        pass

    def test_remove_intervals(self):
        pass
